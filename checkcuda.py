import cupy as cp
print("CuPy version:", cp.__version__)
print("CUDA runtime version:", cp.cuda.runtime.runtimeGetVersion())
print("CUDA driver version:", cp.cuda.runtime.driverGetVersion())
print("Device count:", cp.cuda.runtime.getDeviceCount())
if cp.cuda.runtime.getDeviceCount() > 0:
    props = cp.cuda.runtime.getDeviceProperties(0)
    print("Device 0 name:", props["name"])
