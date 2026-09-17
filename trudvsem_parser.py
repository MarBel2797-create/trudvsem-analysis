import requests
import pandas as pd
import time

def get_vacancies_trudvsem(text, max_pages=20):
    all_vacancies = []
    base_url = "http://opendata.trudvsem.ru/api/v1/vacancies"

    for page in range(max_pages):
        offset = page * 100
        params = {"text": text, "offset": offset, "limit": 100}

        try:
            response = requests.get(base_url, params=params, timeout=15)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка на странице {page} для '{text}': {e}")
            break

        data = response.json()
        vacancies = data.get("results", {}).get("vacancies", [])

        if not vacancies:
            print(f"Запрос '{text}': страница {page+1} пуста, завершаем.")
            break

        for v in vacancies:
            vacancy = v.get("vacancy", {})
            company = vacancy.get("company", {})
            all_vacancies.append({
                "name": vacancy.get("job-name"),
                "company": company.get("name"),
                "region": vacancy.get("region", {}).get("name"),
                "salary_min": vacancy.get("salary_min"),
                "salary_max": vacancy.get("salary_max"),
                "currency": vacancy.get("currency"),
                "date": vacancy.get("date"),
                "url": vacancy.get("vac_url"),
                "requirement": vacancy.get("requirement", {}).get("qualification"),
                "duty": vacancy.get("duty"),
            })

        print(f"Запрос '{text}': страница {page+1}, всего вакансий: {len(all_vacancies)}")
        time.sleep(1)

    return all_vacancies

# --- Сбор по нескольким запросам ---
search_queries = ["аналитик данных", "data analyst", "бизнес-аналитик", "системный аналитик"]
all_vacancies = []

for query in search_queries:
    print(f"\n🔍 Сбор по запросу: '{query}'")
    vacancies = get_vacancies_trudvsem(query, max_pages=10)
    all_vacancies.extend(vacancies)

# Убираем дубликаты по URL
df = pd.DataFrame(all_vacancies)
df = df.drop_duplicates(subset=["url"])

df.to_csv("trudvsem_vacancies.csv", index=False, encoding="utf-8-sig")
print(f"\n✅ Итого собрано уникальных вакансий: {len(df)}")
