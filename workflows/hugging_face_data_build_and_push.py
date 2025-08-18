from lk_acts import HuggingFaceDataset

if __name__ == "__main__":
    hfds = HuggingFaceDataset()
    hfds.build_acts()
    hfds.build_chunks()
    hfds.upload_to_hugging_face()
