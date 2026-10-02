"""Ödeme ve Fatura Mutabakatı.

Problem: Belirsiz ödemeyi rastgele faturaya kapatmadan, ücret ve iade sonrası net tutarı izlemek.
Method: Kısmi tahsis, çoklu referans, kuruş bazlı korunum
Invariant: Tutarlar tamsayı minor unit; açık referans yoksa yalnız bir uygun aday otomatik eşleşir.
Boundary: Kur dönüşümü ve banka entegrasyonu yoktur; toleransla kapanan bakiyeler raporda görünmeye devam eder."""
from collections import defaultdict

def reconcile(invoices, payments, tolerance=1):
    if tolerance < 0:
        raise ValueError('negative tolerance')
    invoice_ids = [i['id'] for i in invoices]
    payment_ids = [p['id'] for p in payments]
    if len(set(invoice_ids)) != len(invoice_ids) or len(set(payment_ids)) != len(payment_ids):
        raise ValueError('duplicate identifiers')
    remaining = {i['id']: i['amount_minor'] for i in invoices}
    byid = {i['id']: i for i in invoices}
    allocations = []
    review = []
    if any((type(v) is not int or v < 0 for v in remaining.values())):
        raise ValueError('nonnegative integer amount required')
    for p in sorted(payments, key=lambda p: (p['day'], p['id'])):
        if type(p['amount_minor']) is not int or p['amount_minor'] < 0:
            raise ValueError('invalid payment amount')
        if any((type(p.get(k, 0)) is not int or p.get(k, 0) < 0 for k in ('fee_minor', 'refund_minor'))):
            raise ValueError('invalid fee/refund')
        net = p['amount_minor'] - p.get('fee_minor', 0) - p.get('refund_minor', 0)
        if net < 0:
            raise ValueError('negative net settlement')
        eligible = [i for i in invoices if i['currency'] == p['currency'] and i['customer'] == p['customer'] and (remaining[i['id']] > 0) and (i['day'] <= p['day'])]
        refs = p.get('invoice_refs', [])
        if refs:
            if len(set(refs)) != len(refs):
                raise ValueError('duplicate allocation reference')
            if any((r not in byid or byid[r] not in eligible for r in refs)):
                review.append({'payment': p['id'], 'reason': 'invalid_or_closed_reference', 'unallocated_minor': net})
                continue
            eligible = [byid[r] for r in refs]
        elif len(eligible) != 1:
            review.append({'payment': p['id'], 'reason': 'ambiguous' if eligible else 'unmatched', 'candidates': [i['id'] for i in eligible], 'unallocated_minor': net})
            continue
        available = net
        for i in eligible:
            applied = min(available, remaining[i['id']])
            available -= applied
            remaining[i['id']] -= applied
            if applied:
                allocations.append({'payment': p['id'], 'invoice': i['id'], 'currency': p['currency'], 'amount_minor': applied})
        if available > tolerance:
            review.append({'payment': p['id'], 'reason': 'overpayment', 'unallocated_minor': available})
        elif available:
            review.append({'payment': p['id'], 'reason': 'rounding_remainder', 'unallocated_minor': available})
    balances = [{'invoice': i['id'], 'currency': i['currency'], 'open_minor': remaining[i['id']], 'status': 'CLOSED' if remaining[i['id']] <= tolerance else 'OPEN'} for i in invoices]
    currencies = sorted({i['currency'] for i in invoices} | {p['currency'] for p in payments})
    controls = []
    for currency in currencies:
        net = sum((p['amount_minor'] - p.get('fee_minor', 0) - p.get('refund_minor', 0) for p in payments if p['currency'] == currency))
        allocated = sum((a['amount_minor'] for a in allocations if a['currency'] == currency))
        unallocated = sum((r['unallocated_minor'] for r in review if next((p['currency'] for p in payments if p['id'] == r['payment'])) == currency))
        if net != allocated + unallocated:
            raise AssertionError('cash conservation failed')
        controls.append({'currency': currency, 'net_minor': net, 'allocated_minor': allocated, 'unallocated_minor': unallocated})
    return {'allocations': allocations, 'balances': balances, 'review': review, 'cash_controls': controls}

def run(config):
    return reconcile(config['invoices'], config['payments'], config.get('tolerance', 1))

import argparse, json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='Run reproducible synthetic project scenario')
    parser.add_argument('command', choices=['demo'])
    parser.add_argument('--input', default='scenario.json')
    parser.add_argument('--output', default='report.json')
    args = parser.parse_args()
    report = run(json.loads(Path(args.input).read_text(encoding='utf-8')))
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')
    print(f'Report: {target}')
if __name__ == '__main__':
    main()
