# Парсер Флампа для заведений и их отзывов

Спарщены заведения Екатеринбурга и Москвы по рубрикам "Еда" и "Бары".

Всего бъектов в выгрузке — 5880, отзывов — 104586

## Структура
```json
[{
    'id',
    'name_primary',
    'name_extension',
    'city',
    'address',
    'rating_decimal',
    'reviews_count',
    'business_lunch',
    'avg_price',
    'reviews': [
        {
            'id',
            'text',
            'user',
            'rating',
            'likes_score',
            'date_created',
            'official_answer': [{
                'text',
                'date_created',
            }]
        }
    ]
}]
```