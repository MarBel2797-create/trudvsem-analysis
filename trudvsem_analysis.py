import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# 1. Загрузка данных
df = pd.read_csv("trudvsem_vacancies.csv")

print(f"Всего вакансий: {len(df)}")
print(f"Колонки: {df.columns.tolist()}")

# 2. Очистка зарплат (0 = не указана)
df["salary_min"] = df["salary_min"].replace(0, None)
df["salary_max"] = df["salary_max"].replace(0, None)

# 3. Топ-10 регионов по количеству вакансий
print("\nТоп-10 регионов:")
top_regions = df["region"].value_counts().head(10)
print(top_regions)

# 4. Топ-10 компаний
print("\nТоп-10 компаний:")
top_companies = df["company"].value_counts().head(10)
print(top_companies)

# 5. Средняя зарплата (по минимальной)
salaries = df["salary_min"].dropna()
if len(salaries) > 0:
    print(f"\nСредняя минимальная зарплата: {salaries.mean():.0f} руб.")
    print(f"Медиана: {salaries.median():.0f} руб.")
    print(f"Минимум: {salaries.min():.0f} руб.")
    print(f"Максимум: {salaries.max():.0f} руб.")
else:
    print("\nЗарплаты не указаны в данных.")

# 6. Поиск навыков в тексте вакансий
skills_keywords = ["SQL", "Python", "Excel", "Power BI", "Tableau",
                   "pandas", "matplotlib", "статистика", "A/B", "ETL", "1С", "Git"]

skill_counts = {skill: 0 for skill in skills_keywords}

for duty in df["duty"].dropna():
    duty_lower = str(duty).lower()
    for skill in skills_keywords:
        if skill.lower() in duty_lower:
            skill_counts[skill] += 1

print("\nЧастота упоминания навыков:")
for skill, count in sorted(skill_counts.items(), key=lambda x: -x[1]):
    if count > 0:
        print(f"{skill}: {count} раз")

# 7. Визуализация
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

top_regions.plot(kind="barh", ax=axes[0], color="skyblue")
axes[0].set_title("Топ-10 регионов по количеству вакансий")
axes[0].set_xlabel("Количество вакансий")

skills_series = pd.Series(skill_counts).sort_values(ascending=True)
skills_series = skills_series[skills_series > 0]
skills_series.plot(kind="barh", ax=axes[1], color="coral")
axes[1].set_title("Частота упоминания навыков")
axes[1].set_xlabel("Количество упоминаний")

plt.tight_layout()
plt.savefig("trudvsem_analysis.png")
plt.show()

print("\nГрафики сохранены в файл trudvsem_analysis.png")
