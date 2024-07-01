import os
import logging

import torch

from DiffuAug.srcs.generation.metrics.fid import compute_fid
from DiffuAug.srcs.generation.metrics.improved_precision_recall import IPR
from DiffuAug.srcs import utility

def main():
    OPTION = "ALL"
    utility.set_seed()
    
    if OPTION == "FID":
        DUKE_DATA_PATH = r"/data/duke_data/size_64/split_datalabel"
        FAKE_DATA_PATH = r"/data/results/generation/sampling/cfg/imbalanced/sampling_imgs/ddim/epoch_70/p_uncond_0.1/w_4.0"
        device = "cuda:0" if torch.cuda.is_available() else "cpu"

        # FID 계산
        fid_result = compute_fid(
            device=device,
            original_data_path=DUKE_DATA_PATH,
            generated_data_path=FAKE_DATA_PATH
            )
        print(f"FID Score: {fid_result:.2f}")
        
    elif OPTION == "PRECISION_RECALL":
        RANDOM_BALANCED_ORIGIN_DATA_PATH = r"/data/duke_data/size_64/random_balanced_origin_data"
        PATH_FAKE = r'/data/results/generation/sampling/cfg/imbalanced/sampling_imgs/ddim/epoch_70/p_uncond_0.1/w_4.0'
        batch_size = 50 # 기존 코드의 defulat 값
        k = 3 # 기존 코드의 defulat 값
        num_samples = 2600 # real, fake에서 feature를 추출할 이미지의 개수
        fname_precalc = ''

        ipr = IPR(batch_size, k, num_samples)
        with torch.no_grad():
            # real
            ipr.compute_manifold_ref(RANDOM_BALANCED_ORIGIN_DATA_PATH) # manifold_ref값을 구해 self.manifold_ref에 저장
            if len(fname_precalc) > 0:
                ipr.save_ref(fname_precalc)
                print('path_fake (%s) is ignored for precalc' % PATH_FAKE)
                exit()

            # fake
            precision, recall = ipr.precision_and_recall(PATH_FAKE)

        print('precision:', precision)
        print('recall:', recall)

    elif OPTION == "ALL":
        LOG_PATH = r"/data/results/generation/metric_log"
        DUKE_DATA_PATH = r"/data/duke_data/size_64/split_datalabel"
        RANDOM_BALANCED_ORIGIN_DATA_PATH = r"/data/duke_data/size_64/random_balanced_origin_data"
        
        SAMPLING_ROOT_PATH = r"/data/results/generation/sampling/cfg/imbalanced/sampling_imgs/ddim/epoch_70/p_uncond_0.2"
        
        utility.set_normal_logger(LOG_PATH)
        device = "cuda:0" if torch.cuda.is_available() else "cpu"

        w_list = [
            0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,
            1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9,
            2.0, 3.0, 4.0
        ]

        # Precision, Recall
        batch_size = 200 # 기존 코드의 defulat 값
        k = 3 # 기존 코드의 defulat 값
        num_samples = 2600 # real, fake에서 feature를 추출할 이미지의 개수
        fname_precalc = ''
        ipr = IPR(batch_size, k, num_samples)
        
        # 지정된 w 값까지 이미지 생성
        for w in w_list:
            fake_path = os.path.join(SAMPLING_ROOT_PATH, f"w_{w}")
            
            print(f"FID 계산, w: {w}")
            logging.info(f"w: {w}")
            
             # FID 계산
            fid_result = compute_fid(
                device=device,
                original_data_path=RANDOM_BALANCED_ORIGIN_DATA_PATH,
                generated_data_path=fake_path
                )
            print(f"FID Score: {fid_result:.2f}")    
            logging.info(f"FID Score: {fid_result:.2f}")
            
            # Precision, Recall 계산
            with torch.no_grad():
                # real
                
                # Real data에 대해 생성된 이미지와 개수를 동일하게 맞추어 계산할 수 있도록 수정
                ipr.compute_manifold_ref(RANDOM_BALANCED_ORIGIN_DATA_PATH) # manifold_ref값을 구해 self.manifold_ref에 저장
                if len(fname_precalc) > 0:
                    ipr.save_ref(fname_precalc)
                    print('path_fake (%s) is ignored for precalc' % fake_path)
                    exit()

                # fake
                precision, recall = ipr.precision_and_recall(fake_path)
            
            print(f"Precision: {precision}, Recall: {recall}")
            logging.info(f"Precision: {precision}, Recall: {recall}\n")
            print(f"\n")
                


if __name__ == '__main__':
    main()