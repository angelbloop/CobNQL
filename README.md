# CobNQL - Blockchain Transaction & OSINT Analyzer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**CobNQL** - мощный инструмент для анализа блокчейн-транзакций и проверки адресов через OSINT-базы. Поддерживает Bitcoin и Ethereum с возможностью расширения на другие сети.

## 🎯 Возможности

- **Анализ транзакций Bitcoin/Ethereum** - Полный парсинг входов, выходов, адресов
- **OSINT Проверка** - Проверка адресов против баз OFAC, миксеров, бирж
- **Граф адресов** - Построение сетевого графа связей и кластеризация
- **Риск-анализ** - Автоматическое обнаружение подозрительных паттернов
- **Гибкий экспорт** - JSON, HTML, CSV, ASCII графики
- **Compliance-ready** - Для SAR отчетов и аудитов

## 📋 Требования

- Python 3.8+
- Интернет соединение (для API запросов)
- API ключ Etherscan (опционально, для Ethereum анализа)

## ⚡ Быстрый старт

### 1. Установка

```bash
git clone https://github.com/angelbloop/CobNQL.git
cd CobNQL
pip install -r requirements.txt
```

### 2. Конфигурация

```bash
cp .env.example .env
# Отредактируйте .env и добавьте свой API ключ (опционально)
```

### 3. Использование

```bash
# Bitcoin анализ
python main.py scan 85f9ba5407d69919357309b54f3411c5b0ceea46a677bc6bf0a1a95b7c0157d0

# OSINT анализ
python main.py osint <tx_hash>
```

## 📁 Структура проекта

```
CobNQL/
├── src/
│   ├── fetchers/          # API интеграция
│   ├── analyzer.py        # Анализ транзакций
│   ├── address_graph.py   # Граф адресов
│   ├── osint_checker.py   # OSINT проверка
│   └── enhanced_reporter.py # Отчеты
├── main.py                # CLI
├── requirements.txt       # Зависимости
└── README.md              # Этот файл
```

## 🔧 API Ключи

Добавьте свои ключи в `config.json`:
- **Etherscan**: https://etherscan.io/apis (free tier доступен)
- **Bitcoin**: Mempool.space (без ключа)

## 📊 Примеры

### Анализ транзакции
```bash
python main.py scan 85f9ba5407d69919357309b54f3411c5b0ceea46a677bc6bf0a1a95b7c0157d0
```

### OSINT проверка
```bash
python main.py osint <tx_hash>
```

## 📝 Лицензия

MIT License - см. [LICENSE](LICENSE)

## 🤝 Контрибьютинг

См. [CONTRIBUTING.md](CONTRIBUTING.md)

---

Сделано с ❤️ для blockchain community