from django import template
from iotdashboard.settings import WEBSITE_NAME
import time
import os

register = template.Library()


@register.simple_tag
def version():
    """
    GIT version
    """
    try:
        return time.strftime('%m%d%Y/%u', time.gmtime(os.path.getmtime('.git/')))
    except:
        return 0


@register.simple_tag
def website_name():
    """
    WEBSITE_NAME = "AirTracker"
    """
    return WEBSITE_NAME
