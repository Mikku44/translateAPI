from transformers import MarianMTModel, MarianTokenizer
import os

model_dir = "./opustcv"

# Verify files exist
required_files = ["source.spm", "target.spm", "vocab.json", "config.json"]
for file in required_files:
    if not os.path.exists(os.path.join(model_dir, file)):
        raise FileNotFoundError(f"Missing file: {file}")

# Load tokenizer with explicit vocab path
tokenizer = MarianTokenizer.from_pretrained(
    model_dir,
    vocab_file=os.path.join(model_dir, "vocab.json"),  # Explicit path
    source_spm=os.path.join(model_dir, "source.spm"),
    target_spm=os.path.join(model_dir, "target.spm")
)

model = MarianMTModel.from_pretrained(model_dir)

def translate(text: str) -> str:
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model.generate(**inputs)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

print(translate("Hello world!"))  # Should output: "สวัสดีชาวโลก"

# from sentencepiece import SentencePieceProcessor

# # Load source SentencePiece model
# sp_source = SentencePieceProcessor()
# sp_source.load(f"{model_dir}/source.spm")

# # Create vocab dictionary
# vocab = {id: sp_source.id_to_piece(id) for id in range(sp_source.get_piece_size())}

# # Save as vocab.json
# import json
# with open(f"{model_dir}/vocab.json", "w") as f:
#     json.dump(vocab, f)