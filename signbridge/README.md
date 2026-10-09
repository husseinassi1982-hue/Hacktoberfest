# SignBridge

React frontend and Python API scaffold for an ASL translation application.

## Status

This is a project scaffold, not a working sign recognizer. Camera capture, hand detection, preprocessing, ONNX classification, and Gemma translation are integration stubs. `backend/models/asl_cnn_model.onnx` is an intentionally empty placeholder, not a trained model. Replace it with licensed trained weights and provide the matching labels and preprocessing contract.

## Frontend

Requires Node.js 20.19+.

```sh
cd signbridge/frontend
npm install
npm run dev
```

Open http://localhost:5173. Set `VITE_API_URL` to override the default backend URL, http://localhost:8000.

## Backend

Requires Python 3.10+.

```sh
cd signbridge/backend
python -m venv .venv
```

Activate the environment (`.venv\\Scripts\\Activate.ps1` on Windows or `source .venv/bin/activate` on macOS/Linux), then:

```sh
pip install -r requirements.txt
uvicorn app:app --reload
```

API health: http://localhost:8000/health. API documentation: http://localhost:8000/docs.

## Next steps

Implement camera capture and hand detection, supply a trained ONNX model, define preprocessing and labels, add recognition routes, and configure a Gemma provider. Keep provider credentials in backend environment variables.
