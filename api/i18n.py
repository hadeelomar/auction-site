"""
Internationalisation utilities for the auction site.
Includes language detection, currency conversion, and locale helpers.
"""
from django.http import JsonResponse, HttpRequest
from django.conf import settings
from django.utils import translation
from django.views.decorators.csrf import csrf_exempt
import json
import os
from decimal import Decimal
from typing import Dict, Any, Optional

# Currency configurations with symbols and exchange rates (base: GBP)
CURRENCIES = {
    'GBP': {'symbol': '£', 'name': 'British Pound', 'rate': 1.0},
    'USD': {'symbol': '$', 'name': 'US Dollar', 'rate': 1.27},
    'EUR': {'symbol': '€', 'name': 'Euro', 'rate': 1.17},
    'CNY': {'symbol': '¥', 'name': 'Chinese Yuan', 'rate': 9.12},
    'JPY': {'symbol': '¥', 'name': 'Japanese Yen', 'rate': 189.50},
    'KRW': {'symbol': '₩', 'name': 'South Korean Won', 'rate': 1680.00},
    'INR': {'symbol': '₹', 'name': 'Indian Rupee', 'rate': 105.50},
    'SAR': {'symbol': 'ر.س', 'name': 'Saudi Riyal', 'rate': 4.76},
    'AED': {'symbol': 'د.إ', 'name': 'UAE Dirham', 'rate': 4.66},
    'ILS': {'symbol': '₪', 'name': 'Israeli Shekel', 'rate': 4.72},
    'RUB': {'symbol': '₽', 'name': 'Russian Ruble', 'rate': 113.00},
    'BRL': {'symbol': 'R$', 'name': 'Brazilian Real', 'rate': 6.35},
    'TRY': {'symbol': '₺', 'name': 'Turkish Lira', 'rate': 38.50},
}

# Language to default currency mapping
LANGUAGE_CURRENCY_MAP = {
    'en': 'GBP',
    'ar': 'SAR',
    'he': 'ILS',
    'zh-hans': 'CNY',
    'zh-hant': 'CNY',
    'es': 'EUR',
    'fr': 'EUR',
    'de': 'EUR',
    'ja': 'JPY',
    'ko': 'KRW',
    'pt': 'EUR',
    'ru': 'RUB',
    'hi': 'INR',
    'tr': 'TRY',
}

# RTL languages
RTL_LANGUAGES = ['ar', 'he']


def get_supported_languages(request: HttpRequest) -> JsonResponse:
    """
    GET /api/i18n/languages
    Returns list of supported languages with their details.
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    languages = []
    for code, name in settings.LANGUAGES:
        languages.append({
            'code': code,
            'name': name,
            'isRTL': code in RTL_LANGUAGES,
            'defaultCurrency': LANGUAGE_CURRENCY_MAP.get(code, 'GBP')
        })

    current_language = translation.get_language() or 'en'

    return JsonResponse({
        'languages': languages,
        'currentLanguage': current_language,
        'isRTL': current_language in RTL_LANGUAGES
    })


def get_supported_currencies(request: HttpRequest) -> JsonResponse:
    """
    GET /api/i18n/currencies
    Returns list of supported currencies with exchange rates.
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    currencies = []
    for code, details in CURRENCIES.items():
        currencies.append({
            'code': code,
            'symbol': details['symbol'],
            'name': details['name'],
            'rate': details['rate']
        })

    return JsonResponse({
        'currencies': currencies,
        'baseCurrency': 'GBP'
    })


def convert_currency(request: HttpRequest) -> JsonResponse:
    """
    GET /api/i18n/convert?amount=100&from=GBP&to=USD
    Convert amount between currencies.
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    amount_str = request.GET.get('amount', '0')
    from_currency = request.GET.get('from', 'GBP').upper()
    to_currency = request.GET.get('to', 'USD').upper()

    try:
        amount = Decimal(amount_str)
    except:
        return JsonResponse({'error': 'Invalid amount'}, status=400)

    if from_currency not in CURRENCIES:
        return JsonResponse({'error': f'Unsupported currency: {from_currency}'}, status=400)
    if to_currency not in CURRENCIES:
        return JsonResponse({'error': f'Unsupported currency: {to_currency}'}, status=400)

    # Convert to GBP first, then to target currency
    from_rate = Decimal(str(CURRENCIES[from_currency]['rate']))
    to_rate = Decimal(str(CURRENCIES[to_currency]['rate']))

    # amount in GBP
    gbp_amount = amount / from_rate
    # convert to target
    converted = gbp_amount * to_rate

    return JsonResponse({
        'originalAmount': str(amount),
        'convertedAmount': str(round(converted, 2)),
        'fromCurrency': from_currency,
        'toCurrency': to_currency,
        'symbol': CURRENCIES[to_currency]['symbol'],
        'formatted': f"{CURRENCIES[to_currency]['symbol']}{round(converted, 2):,.2f}"
    })


def set_language(request: HttpRequest) -> JsonResponse:
    """
    POST /api/i18n/language
    Set user's preferred language.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    language = data.get('language', 'en')

    # Validate language code
    valid_codes = [code for code, _ in settings.LANGUAGES]
    if language not in valid_codes:
        return JsonResponse({'error': f'Unsupported language: {language}'}, status=400)

    # Activate the language
    translation.activate(language)

    # Set language in session using Django's standard key
    request.session['_language'] = language

    response = JsonResponse({
        'message': 'Language updated',
        'language': language,
        'isRTL': language in RTL_LANGUAGES
    })

    # Also set cookie for persistence
    response.set_cookie(
        'django_language',
        language,
        max_age=31536000  # 1 year
    )

    return response


def get_locale_data(request: HttpRequest) -> JsonResponse:
    """
    GET /api/i18n/locale
    Get complete locale data for current user including language, currency, and formatting.
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    current_language = translation.get_language() or 'en'
    is_rtl = current_language in RTL_LANGUAGES

    # Get preferred currency from session or default based on language
    preferred_currency = request.session.get(
        'preferred_currency',
        LANGUAGE_CURRENCY_MAP.get(current_language, 'GBP')
    )

    currency_data = CURRENCIES.get(preferred_currency, CURRENCIES['GBP'])

    return JsonResponse({
        'language': {
            'code': current_language,
            'isRTL': is_rtl,
            'direction': 'rtl' if is_rtl else 'ltr'
        },
        'currency': {
            'code': preferred_currency,
            'symbol': currency_data['symbol'],
            'name': currency_data['name']
        },
        'formatting': {
            'dateFormat': 'DD/MM/YYYY' if current_language in ['en', 'ar', 'he'] else 'YYYY-MM-DD',
            'timeFormat': '24h' if current_language in ['de', 'fr', 'es'] else '12h',
            'numberSeparator': ',' if current_language == 'en' else '.'
        }
    })


def set_currency(request: HttpRequest) -> JsonResponse:
    """
    POST /api/i18n/currency
    Set user's preferred currency.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    currency = data.get('currency', 'GBP').upper()

    if currency not in CURRENCIES:
        return JsonResponse({'error': f'Unsupported currency: {currency}'}, status=400)

    # Store in session
    request.session['preferred_currency'] = currency

    return JsonResponse({
        'message': 'Currency updated',
        'currency': currency,
        'symbol': CURRENCIES[currency]['symbol']
    })
