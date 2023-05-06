import YaUploader_class, common_func as C_F, VK_class as V_K

if __name__ == '__main__':
    uploader = YaUploader_class.YaUploader(C_F.get_settings('Ytoken'))
    uploader.Backup_VKphoto_to_YDisk(count = 7)

    





