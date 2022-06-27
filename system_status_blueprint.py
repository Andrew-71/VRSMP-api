from flask import Blueprint

import psutil

system_stats = Blueprint('system_stats', __name__)


@system_stats.route('/system_status')
def get_system_status():

    cpu_percent = psutil.cpu_percent()

    memory = psutil.virtual_memory()
    memory_available = round(memory.available/1024.0/1024.0,1)
    memory_total = round(memory.total/1024.0/1024.0,1)
    memory_units = 'MB'

    disk = psutil.disk_usage('/')
    disk_free = round(disk.free/1024.0/1024.0/1024.0,1)
    disk_total = round(disk.total/1024.0/1024.0/1024.0,1)
    disk_units = 'GB'

    return {'cpu_percent': cpu_percent,
            'memory': {'available': memory_available, 'total': memory_total, 'units': memory_units},
            'disk': {'free': disk_free, 'total': disk_total, 'units': disk_units},
            'boot_time': psutil.boot_time()}