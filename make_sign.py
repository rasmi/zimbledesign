import argparse
import requests
import re


base_url = 'http://signmaking.rockler.com/'
sign_path = 'base.cfc?method=getTemplate&returnFormat=json'


def request_sign_data(sign_text):
  data = {'stringIn': sign_text}
  sign_url = '{}{}'.format(base_url, sign_path)
  r = requests.post(sign_url, data=data)

  return r.json()


def get_pdf_url(response_text):
  pdf_pattern = r'href="(base2\.cfc\?method=displayPDF&g=[\w-]*)"'
  pdf_regex = re.compile(pdf_pattern)
  results = pdf_regex.findall(response_text)

  if results:
    pdf_id = results[0]
    pdf_url = '{}{}'.format(base_url, pdf_id)

    return pdf_url


def download_pdf(pdf_url, file_path):
  pdf_file = requests.get(pdf_url)

  with open(file_path, 'wb') as f:
      f.write(pdf_file.content)


def create_sign_pdf(text):
  sign_data = request_sign_data(text)
  sign_pdf_url = get_pdf_url(sign_data)

  if sign_pdf_url:
    download_pdf(sign_pdf_url, 'sign_{}.pdf'.format(text))
  else:
    raise Exception('No sign found for text: {}'.format(text))


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('text', type=str, help='Sign text to generate.')
  args = parser.parse_args()
  text = args.text

  create_sign_pdf(text)
