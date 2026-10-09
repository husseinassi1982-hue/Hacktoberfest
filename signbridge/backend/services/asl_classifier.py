"""ASL ONNX inference integration point."""
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "asl_cnn_model.onnx"

def classify_sign(hand_image):
    """Load a trained model and its label mapping before implementing inference."""
    raise NotImplementedError("The ONNX file is an empty placeholder; supply a trained model.")
