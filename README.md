# theia.ai
iOS application to aid the visually impaired traverse external environments. The app uses a DeepLabV3+MobileNetV2 model trained on the Cityscapes dataset for inference. This application is based on and inspired by [blindassist-ios](https://github.com/BlindAssist/blindassist-ios).

## Instructions
Currently works only on simulator.
1. Run `TheiaModel/app.py`. Server is launched on `localhost`.
2. Launch Theia on simulator.

## TODO

- [ ] Add Camera module instead of photopicker.
- [ ] Run model on device locally using CoreML.
- [ ] Incorporate ARKit for depth data.
- [ ] Improve algorithm to predict next action to perform.
- [ ] Expand to diverse environments, not only areas of traffic/roads.
