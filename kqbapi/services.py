import requests

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
