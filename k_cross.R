library(WVPlots)
library(pROC)
library(PRROC)

# Revised: k-fold (file-based) evaluation that keeps all metric calculations
compare_cv_structure <- function(
    train_path_template = "filtered_lichess/eval_db_filtered_train[1].csv",
    validate_path_template = "filtered_lichess/eval_db_filtered_validate[1].csv",
    thresh = 0.5,
    factors = paste0("Factor_", 1:7),
    k = 5,
    make_plots = FALSE
) {
  # Helper to build formula text from factors (always full model here)
  build_form <- function(fs) as.formula(paste("side ~", paste(fs, collapse = " + ")))
  form <- build_form(factors)
  
  # store per-fold results
  fold_results <- list()
  
  # log-likelihood helper
  loglikelihood <- function(y, py) {
    sum(y * log(py) + (1 - y) * log(1 - py))
  }
  
  for (i in seq_len(k)) {
    train_path <- gsub("\\[1\\]", paste0("[", i, "]"), train_path_template)
    validate_path <- gsub("\\[1\\]", paste0("[", i, "]"), validate_path_template)
    
    dt <- read.csv(train_path)
    dv <- read.csv(validate_path)
    
    # ---- Fit model ----
    model <- glm(form, family = binomial(link = logit), data = dt)
    
    # ---- TRAIN predictions ----
    dt$pred_prob <- predict(model, newdata = dt, type = "response")
    if (make_plots) {
      DoubleDensityPlot(dt, "pred_prob", "side", title = paste0("Distribution of side predictions (train) - fold ", i))
    }
    dt$pred_class <- ifelse(dt$pred_prob >= thresh, 1, 0)
    dt$pred_class <- factor(dt$pred_class, levels = c(0,1))
    
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
    
    null_dev_model <- model$null.deviance
    resid_dev_model <- model$deviance
    fisher_iter <- model$iter
    model_aic <- AIC(model)
    
    pseudo_r2_train <- 1 - (resid_dev_model / null_dev_model)
    
    testy <- as.numeric(dv$side)
    pnull_test <- mean(testy)
    null_dev_test <- -2 * loglikelihood(testy, pnull_test)
    resid_dev_test <- -2 * loglikelihood(testy, dv$pred_prob)
    pseudo_r2_val <- 1 - (resid_dev_test / null_dev_test)
    
    fold_results[[i]] <- data.frame(
      model = paste0("fold_", i),
      dropped = "(none)",
      n_factors = length(factors),
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
  
  combined <- do.call(rbind, fold_results)
  num_cols <- sapply(combined, is.numeric)
  averaged <- as.list(colMeans(combined[, num_cols, drop = FALSE], na.rm = TRUE))
  
  result_row <- data.frame(
    model = "full_cv",
    dropped = "(none)",
    n_factors = length(factors),
    stringsAsFactors = FALSE
  )
  
  for (nm in names(combined)[num_cols]) {
    result_row[[nm]] <- averaged[[nm]]
  }
  
  return(result_row)
}

# ---- call ----
res <- compare_cv_structure(
  train_path_template = "filtered_lichess/eval_db_filtered_train[1].csv",
  validate_path_template = "filtered_lichess/eval_db_filtered_validate[1].csv",
  thresh = 0.5,
  factors = paste0("Factor_", 1:7),
  k = 5,
  make_plots = FALSE
)
print(res)
