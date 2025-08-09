import os, shutil, subprocess, sys
def _run(cmd):
  print("[SDR-DEP] $"," ".join(cmd))
  try:
    subprocess.check_call(cmd); return True
  except Exception as e:
    print("[SDR-DEP] WARN:", e); return False
def _which(x): return shutil.which(x) is not None

APT = ["build-essential","pkg-config","portaudio19-dev","libusb-1.0-0-dev","libudev-dev","libssl-dev","qmake","scons","ffmpeg","python3-dev"]
PIP = ["opencv-python","ffmpeg-python","pyaudio","pycapnp","pre-commit","pytest"]

def ensure_system():
  if not _which("apt-get"): print("[SDR-DEP] apt-get not found"); return
  _run(["sudo","apt-get","update"])
  _run(["sudo","apt-get","install","-y"]+APT)

def ensure_python():
  _run([sys.executable," -m","pip","install","--upgrade","pip","setuptools","wheel"])
  _run([sys.executable," -m","pip","install"]+PIP)

def rebuild_capnp():
  if _which("scons"):
    _run(["scons","-u","cereal"])
    _run(["scons","-u","common/params_pyx.so"])
  else:
    print("[SDR-DEP] scons not found")

def ensure_all():
  try:
    from openpilot.common.params import Params
    if Params().get("SDRDepsDone")==b"1":
      print("[SDR-DEP] already done"); return
  except Exception: pass
  ensure_system(); ensure_python(); rebuild_capnp()
  try:
    from openpilot.common.params import Params
    Params().put("SDRDepsDone","1")
  except Exception: pass

if __name__=="__main__": ensure_all()
