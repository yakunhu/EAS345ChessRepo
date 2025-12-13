library(WVPlots)
library(pROC)
library(PRROC)

compare_drop1_structure <- function(
    train_path = "../filtered_lichess/eval_db_filtered_train[1].csv",
    validate_path = "../filtered_lichess/eval_db_filtered_validate[1].csv",
    factors = paste0("Factor_", 1:7),
    thresh = 0.5,
    rank_by = c("val_auc", "val_accuracy", "val_f1"),
    make_plots = FALSE
) {
  rank_by <- match.arg(rank_by)
  
  # Load data
  dt <- read.csv(train_path)
  dv <- read.csv(validate_path)
  
  # Helper to build formula text from factors
  build_form <- function(fs) as.formula(paste("side ~", paste(fs, collapse = " + ")))
  
  # Candidate models: full + drop-one per factor
  candidates <- list(
    list(name = "full", dropped = NA_character_, fs = factors)
  )
  for (f in factors) {
    candidates[[length(candidates) + 1]] <- list(
      name = paste0("drop_", f), dropped = f, fs = setdiff(factors, f)
    )
  }
  
  # Storage for results
  results <- list()
  
  # Loop over each candidate model
  for (cand in candidates) {
    form <- build_form(cand$fs)
    
    # ---- Fit model ----
    model <- glm(form, family = binomial(link = logit), data = dt)
    
    # ---- TRAIN predictions ----
    dt$pred_prob <- predict(model, newdata = dt, type = "response")
    if (make_plots) {
      DoubleDensityPlot(dt, "pred_prob", "side", title = "Distribution of side predictions (train)")
    }
    dt$pred_class <- ifelse(dt$pred_prob >= thresh, 1, 0)
    dt$pred_class <- factor(dt$pred_class, levels = c(0,1))
    
    # Train confusion + metrics
    conf_mat_tr <- table(Actual = dt$side, Predicted = dt$pred_class)
    accuracy_tr <- sum(diag(conf_mat_tr)) / sum(conf_mat_tr)
    precision_tr <- conf_mat_tr[2,2]/(conf_mat_tr[2,2]+conf_mat_tr[1,2])
    recall_tr <- conf_mat_tr[2,2]/(conf_mat_tr[2,2]+conf_mat_tr[2,1])
    enrichment_tr <- precision_tr/mean(as.numeric(dt$side))
    f1_tr <- (2*precision_tr*recall_tr)/(precision_tr+recall_tr)
    
    roc_tr <- roc(dt$side, dt$pred_prob)
    auc_tr <- as.numeric(auc(roc_tr))
    
    pr_tr <- pr.curve(scores.class0 = dt$pred_prob[dt$side==1],
                      scores.class1 = dt$pred_prob[dt$side==0],
                      curve = FALSE)
    pr_auc_tr <- pr_tr$auc.integral
    
    # ---- VALIDATION predictions ----
    dv$pred_prob <- predict(model, newdata = dv, type = "response")
    dv$pred_class <- ifelse(dv$pred_prob >= thresh, 1, 0)
    dv$pred_class <- factor(dv$pred_class, levels = c(0,1))
    
    conf_mat <- table(Actual = dv$side, Predicted = dv$pred_class)
    accuracy <- sum(diag(conf_mat)) / sum(conf_mat)
    precision <- conf_mat[2,2]/(conf_mat[2,2]+conf_mat[1,2])
    recall <- conf_mat[2,2]/(conf_mat[2,2]+conf_mat[2,1])
    enrichment <- precision/mean(as.numeric(dv$side))
    f1 <- (2*precision*recall)/(precision+recall)
    
    roc_obj <- roc(dv$side, dv$pred_prob)
    auc_val <- as.numeric(auc(roc_obj))
    
    pr <- pr.curve(scores.class0 = dv$pred_prob[dv$side==1],
                   scores.class1 = dv$pred_prob[dv$side==0],
                   curve = FALSE)
    pr_auc_val <- pr$auc.integral
    
    # Log-likelihood helpers 
    loglikelihood <- function(y, py) {
      sum(y * log(py) + (1 - y) * log(1 - py))
    }
    
    # Deviance values
    null_dev_model <- model$null.deviance
    resid_dev_model <- model$deviance
    
    # Fisher iterations from model
    fisher_iter <- model$iter
    
    # AIC
    model_aic <- AIC(model)
    
    # Pseudo R^2 (McFadden's)
    pseudo_r2_train <- 1 - (resid_dev_model / null_dev_model)
    
    # Validation pseudo R^2 using deviance computed from validation set
    testy <- as.numeric(dv$side)
    pnull_test <- mean(testy)
    null_dev_test <- -2 * loglikelihood(testy, pnull_test)
    resid_dev_test <- -2 * loglikelihood(testy, dv$pred_prob)
    pseudo_r2_val <- 1 - (resid_dev_test / null_dev_test)
    
    # Assemble a result row
    results[[length(results) + 1]] <- data.frame(
      model = cand$name,
      dropped = ifelse(is.na(cand$dropped), "(none)", cand$dropped),
      n_factors = length(cand$fs),
      train_accuracy = accuracy_tr,
      train_precision = precision_tr,
      train_recall = recall_tr,
      train_enrichment = enrichment_tr,
      train_f1 = f1_tr,
      train_auc = auc_tr,
      train_pr_auc = pr_auc_tr,
      val_accuracy = accuracy,
      val_precision = precision,
      val_recall = recall,
      val_enrichment = enrichment,
      val_f1 = f1,
      val_auc = auc_val,
      val_pr_auc = pr_auc_val,
      null_dev_model = null_dev_model,
      resid_dev_model = resid_dev_model,
      null_dev_test = null_dev_test,
      resid_dev_test = resid_dev_test,
      fisher_iterations = fisher_iter,
      aic = model_aic,
      train_pseudo_r2 = pseudo_r2_train,
      val_pseudo_r2 = pseudo_r2_val,
      stringsAsFactors = FALSE
    )
  }
  
  out <- do.call(rbind, results)
  
  # Simple ranking (structure only; uses existing metrics)
  ord <- switch(rank_by,
                val_auc = order(-out$val_auc, -out$val_pr_auc),
                val_accuracy = order(-out$val_accuracy, -out$val_auc),
                val_f1 = {
                  f1 <- with(out, ifelse((val_precision + val_recall) == 0,
                                         NA_real_, 2 * val_precision * val_recall / (val_precision + val_recall)))
                  order(-f1, -out$val_auc)
                })
  out <- out[ord, , drop = FALSE]
  rownames(out) <- NULL
  view(dt)
  return(out)
}

# ---- call ----
res <- compare_drop1_structure(
  train_path = "../filtered_lichess/eval_db_filtered_train[1].csv",
  validate_path = "../filtered_lichess/eval_db_filtered_validate[1].csv",
  factors = paste0("Factor_", 1:7),
  thresh = 0.5,
  rank_by = "val_auc",
  make_plots = FALSE
)
print(res)
