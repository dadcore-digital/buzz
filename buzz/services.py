from datetime import datetime, timedelta
import pytz
import requests
from django.urls import reverse


def convert_et_to_utc(date_obj):
    """Convert a datetime object from Eastern to UTC."""
    tz = pytz.timezone('US/Eastern')
    now = pytz.utc.localize(datetime.utcnow())
    is_edt = date_obj.astimezone(tz).dst() != timedelta(0)

    if is_edt:
        utc_date = date_obj + timedelta(hours=4) 
    else:
        utc_date = date_obj + timedelta(hours=5) 

    # Tag UTC time zone
    utc_date = utc_date.replace(tzinfo=pytz.UTC)
    return utc_date

def get_sheet_csv(sheets_url, output_filename=None, write_to_file=False):
    """
    Access a publicly available googlesheet tab of match data and save as CSV.
    
    Arguments:
    sheets_url -- A specially crafted URL that provides a CSV export of a google sheet
           tab.
    output_filename -- Save CSV to this filename (str)
    """
    resp = requests.get(sheets_url)
    
    if write_to_file:
        with open(output_filename, 'wb') as fd:
            for chunk in resp.iter_content(chunk_size=128):
                fd.write(chunk)

        return output_filename
    
    else:
        return resp.text


def get_object_admin_link(obj, link_text):
    url = reverse(
        f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change',
        args=[obj.id]
    )
    
    link = f'<a href="{url}">{link_text}</a>'
    return link
    