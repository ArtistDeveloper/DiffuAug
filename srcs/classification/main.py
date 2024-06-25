from DiffuAug.srcs.classification.train.train import train
from DiffuAug.srcs.classification.metrics.roc_curve import *
from DiffuAug.srcs import utility

def main():
    YAML_PATH = r"/workspace/DiffuAug/exp_settings/configs/classification/normal_test_settings/slice/balanced/resnet18_total_200.yaml"
    OPTION = "train"
    
    utility.set_seed()
    cfg = utility.load_config(YAML_PATH)    
    cfg = utility.dict2namespace(cfg)
    
    if OPTION == "train":
        train(cfg)
        
    elif OPTION == "test":
        pred_result_csv_path = r"/data/results/classification/exps/aug/slices/balanced/o200+aug50+aug50/predict_result/predicted_best_30.csv"
        save_curve_png_path = r"/data/results/classification/exps/aug/slices/balanced/o200+aug50+aug50/plot"
    
        # draw_roc_curve(pred_result_csv_path, save_curve_png_path)
        sensitivity, specificity, roc_auc = compute_auc_with_slices(pred_result_csv_path)
        acc = compute_acc_with_slices(pred_result_csv_path)
        
        print(f"AUC: {roc_auc:.2f}, Sensitivity: {sensitivity:.2f}, Specificity: {specificity:.2f}\n")
        print(f"Accuracy: {acc:.2f}\n")


if __name__ == '__main__':
    main()