import torch
from fairseq.models.transformer import TransformerModel

# โหลดโมเดล (English ↔ Thai)
en2th = TransformerModel.from_pretrained(
    model_name_or_path='https://dl.fbaipublicfiles.com/fairseq/models/transformer.wmt19.en-th.tar.gz',
    checkpoint_file='model.pt',
    data_name_or_path='data-bin'
)
th2en = TransformerModel.from_pretrained(
    model_name_or_path='https://dl.fbaipublicfiles.com/fairseq/models/transformer.wmt19.th-en.tar.gz',
    checkpoint_file='model.pt',
    data_name_or_path='data-bin'
)

# ให้โมเดลทำงานบน CPU หรือ CUDA
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
en2th.to(device)
th2en.to(device)

# แปลจากอังกฤษ → ไทย
text_en = "I would like to order some food."
translated_th = en2th.translate(text_en)
print("EN → TH:", translated_th)

# แปลจากไทย → อังกฤษ
text_th = "ฉันอยากสั่งอาหาร"
translated_en = th2en.translate(text_th)
print("TH → EN:", translated_en)
