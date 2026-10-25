"""Local diagnostic prerequisites; provider/host access must be verified separately."""
import argparse,importlib.util,json,shutil,sys

def capabilities():
    return {'python':{'available':sys.version_info>=(3,10),'version':sys.version.split()[0]},
            'pillow':{'available':importlib.util.find_spec('PIL') is not None},
            'ffmpeg':{'available':shutil.which('ffmpeg') is not None},
            'image_generation':{'status':'unknown','verification':'verify selected provider and permissions; no provider bundled'},
            'public_research':{'status':'unknown','verification':'verify assistant search/browser access'},
            'native_size_playback':{'status':'unknown','verification':'requires actual viewing, not successful decode'},
            'host_import':{'status':'unknown','verification':'optional external adapter; no installation or upload performed'},
            'openai_v2_export':{'available':True,'scope':'registered-frame assembly, structural validation and source previews; not generation or installation'},
            'scope':'diagnostics plus independent OpenAI v2 export; provider, visual review and host write access verified separately'}
if __name__=='__main__':
    argparse.ArgumentParser(description=__doc__).parse_args();print(json.dumps(capabilities(),indent=2))
