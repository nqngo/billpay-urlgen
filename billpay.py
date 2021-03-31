#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate a URL for PostBillPay to paste in your web browser."""

import os
import click
import yaml


BASEURL = "https://paypaperbills.postbillpay.com.au/postbillpay/pay/default"


@click.command()
@click.option("-f", "--datafile", help="The Yaml file that store payment profile.", default="default.yaml")
@click.option("-am", "--amount", help="Payment amount", type=click.FLOAT)
@click.option("-bc", "--biller", help="Biller code", type=click.INT)
@click.option("-rn", "--reference", help="Reference number")
@click.option("-m", "--paymentmethod", help="Payment Method", default="PayPal")
@click.option("-e", "--email", help="The email address to send receipt")
def cli(datafile, amount, biller, reference, paymentmethod, email):
  """Generate a URL for PostBillPay page."""
  # Create datafile if not existed
  with open(datafile, "a+") as f:
    f.write('')
  # Otherwise fetch the file
  with open(datafile, "r+") as f:
    data = yaml.safe_load(f)

    # Build a new yaml object if empty
    if data is None:
      data = {
        'amount': None,
        'biller': None,
        'reference': None,
        'paymentmethod': None,
        'email': None
      }

    data['amount'] = data['amount'] if amount is None else amount
    data['biller'] = data['biller'] if biller is None else biller
    data['reference'] = data['reference'] if reference is None else reference.replace(' ', '')
    data['paymentmethod'] = paymentmethod
    data['email'] = data['email'] if email is None else email.replace(' ','')
    
    # Prompt if no value is entered.
    if amount is None and biller is None and reference is None and email is None:
      data['amount'] = click.prompt('Payment amount', type=click.FLOAT, default=data['amount'])
      data['biller'] = click.prompt('Billpay code', type=click.INT, default=data['biller'])
      data['reference'] = click.prompt('Reference no', default=data['reference']).replace(' ', '')
      data['paymentmethod'] = click.prompt('Payment method', default=data['paymentmethod'])
      data['email'] = click.prompt('Receipt email address', default=data['email'])

    # Generate the link
    params = [f"paymentMethod={data['paymentmethod']}"]
    if data['amount'] is not None:
      params.append(f"AP:AM={data['amount']}")
    if data['biller'] is not None:
      params.append(f"AP:BC={data['biller']}")
    if data['reference'] is not None:
      params.append(f"AP:RN={data['reference']}")
    if data['email'] is not None:
      params.append(f"emailAddress={data['email']}")
    click.secho(f"{BASEURL}?{'&'.join(params)}", fg='green')

    # Return to the beginning of the file
    f.seek(0, 0)
    yaml.safe_dump(data, f)