from datasets import load_dataset
import random


def load_opc_dataset(n=100):
    dataset = load_dataset("OpenCoder-LLM/opc-sft-stage2", "educational_instruct")['train']
    length = len(dataset)
    index = list(range(length))
    random.shuffle(index)
    index = index[:n]
    dataset = dataset.select(index)

    return dataset


def load_given_opc_data(seq_id):
    dataset = load_dataset("OpenCoder-LLM/opc-sft-stage2", "educational_instruct")['train']
    for data in dataset:
        if data['seq_id'] == seq_id:
            return data

    raise ValueError(f"Data with seq_id {seq_id} not found in the dataset.")
