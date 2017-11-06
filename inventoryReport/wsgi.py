import os,sys,site

from django.core.wsgi import get_wsgi_application

site.addsitedir("/home/ubuntu/.virutalenvs/iso-inventory-report/lib/python3.5/site-packages")

sys.path.append("/home/ubuntu/iso-inventory-report")
sys.path.append("/home/ubuntu/iso-inventory-report/inventoryReport")

activate_this = "/home/ubuntu/.virtualenvs/iso-inventory-report/bin/activate_this.py"
with open(activate_this) as f:
    code = compile(f.read(), activate_this, "exec")
    exec(code, dict(__file__=activate_this))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inventoryReport.settings")

application = get_wsgi_application()
