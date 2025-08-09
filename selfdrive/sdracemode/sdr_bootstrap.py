import compileall, sys
from importlib import import_module
from .sdr_dependencies import ensure_all

def main():
  print("[SDR-BOOT] ensuring deps…")
  try: ensure_all()
  except Exception as e: print("[SDR-BOOT] deps warn:", e)
  print("[SDR-BOOT] compile…")
  ok = compileall.compile_dir("selfdrive/sdracemode", force=True, quiet=1)
  if not ok: sys.exit("[SDR-BOOT] compile failed")
  print("[SDR-BOOT] smoke import…")
  for m in ["sdracemode","sdracemode_ui","sdracemode_recorder","sdracemode_settings","sdracemode_evcontrols","sdracemode_disclaimer","sdracemode_autoconfig","sdr_autolog"]:
    try: import_module(f"selfdrive.sdracemode.{m}")
    except Exception as e: print("[SDR-BOOT] warn import", m, e)
  print("[SDR-BOOT] ✅ done")

if __name__=="__main__": main()
