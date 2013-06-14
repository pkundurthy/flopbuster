

import os

os.system('cat header.common.html > index.html')
os.system('cat body.index.html >> index.html')
os.system('cat footer.common.html >> index.html')

os.system('cat header.common.html > app.html')
os.system('cat body.app.html >> app.html')
os.system('cat footer.common.html >> app.html')

os.system('cat header.common.html > about.html')
os.system('cat body.about.html >> about.html')
os.system('cat footer.common.html >> about.html')




