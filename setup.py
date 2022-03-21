from cx_Freeze import setup, Executable

setup(name = "Injury Severity Calculator" ,
      version = "1.0.0" ,
      description = "Application that calculates various injury severity scores - APACHE III, SOFA, Charlson Comorbidity"
                    " Index." ,
      executables = [Executable("PYTHON FILE", base = "Win32GUI")]
)