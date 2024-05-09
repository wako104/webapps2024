from rest_framework.decorators import api_view
from rest_framework.response import Response

RATES = {
	'GBP': {'USD': 1.26, 'EUR': 1.17},
	'USD': {'GBP': 0.79, 'EUR': 0.93},
	'EUR': {'GBP': 0.86, 'USD': 1.08}
}


@api_view(['GET'])
def convert_currency(request, from_currency, to_currency, amount):
	if from_currency == to_currency:
		return Response({'converted_amount': float(amount)})

	if from_currency in RATES and to_currency in RATES[from_currency]:
		conversion_rate = RATES[from_currency][to_currency]
		converted_amount = float(amount) * conversion_rate
		return Response({'converted_amount': round(converted_amount, 2)})

	return Response({'error': 'Conversion rate not found'}, status=404)

