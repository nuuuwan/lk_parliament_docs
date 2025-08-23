from lk_acts import HuggingFaceDataset

if __name__ == "__main__":
    hfds = HuggingFaceDataset()
    hfds.build_and_upload(do_upload=True)
