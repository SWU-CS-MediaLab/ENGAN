#-*-coding:utf-8-*-

import os
import argparse
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from trainer import Trainer
from tester import Tester
from utils import create_folder, setup_seed
from config import get_config
import torch
from munch import Munch
from data_loader import get_train_loader, get_test_loader


def main(args):
    # for fast training.
    torch.backends.cudnn.benchmark = True

    setup_seed(args.seed)
    
    # 创建目录
    create_folder(args.save_root_dir, args.version, args.model_save_path)
    create_folder(args.save_root_dir, args.version, args.sample_path)
    create_folder(args.save_root_dir, args.version, args.log_path)
    create_folder(args.save_root_dir, args.version, args.val_result_path)
    create_folder(args.save_root_dir, args.version, args.test_result_path)

    # 生成字典
    if args.mode == 'train':
        loaders = Munch(ref=get_train_loader(root=args.train_img_dir,
                                             img_size=args.image_size,
                                             resize_size=args.resize_size,
                                             batch_size=args.train_batch_size,
                                             shuffle=args.shuffle,
                                             num_workers=args.num_workers,
                                             drop_last=args.drop_last),
                        val=get_test_loader(root=args.val_img_dir,
                                            batch_size=args.val_batch_size,
                                            shuffle=True,
                                            num_workers=args.num_workers))
        trainer = Trainer(loaders, args)
        trainer.train()
    elif args.mode == 'test':
        loaders = Munch(tes=get_test_loader(root=args.test_img_dir,
                                            img_size=args.test_img_size,
                                            batch_size=args.val_batch_size,
                                            shuffle=True,
                                            num_workers=args.num_workers))
        tester = Tester(loaders, args)
        tester.test()
    else:
        raise NotImplementedError('Mode [{}] is not found'.format(args.mode))


if __name__ == '__main__':

    args = get_config()
    
    if args.is_print_network:
        print(args)
        
    main(args)