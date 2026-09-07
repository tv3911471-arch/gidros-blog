#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Собирает content_plan.csv и PLAN.md из курируемого списка тем (Фаза 1)."""
import csv
from pathlib import Path

ROOT = Path(__file__).parent

# (cluster, slug, title, target_query, tier, gate)
# gate: "" = готово к написанию | price | decision | geo
PLAN = [
# --- Скважина: базовое / инфо ---
("skvazhina-osnovy","skvazhina-na-vodu-pod-klyuch","Скважина на воду под ключ: что входит в работы и от чего зависит результат","скважина на воду под ключ","СЧ",""),
("skvazhina-osnovy","kolodec-ili-skvazhina","Колодец или скважина: что выбрать для загородного дома","колодец или скважина","ВЧ",""),
("skvazhina-osnovy","kakoj-glubiny-byvaet-skvazhina-v-podmoskovje","Какой глубины бывает скважина на воду в Подмосковье","какой глубины скважина","СЧ",""),
("skvazhina-osnovy","skvazhina-na-pesok-ili-na-izvestnyak","Скважина на песок или на известняк: разница, срок службы, цена","скважина на песок или известняк","СЧ",""),
("skvazhina-osnovy","artezianskaya-skvazhina-chto-eto","Артезианская скважина: что это, плюсы и срок службы","артезианская скважина что это","СЧ",""),
("skvazhina-osnovy","abissinskaya-skvazhina-kogda-podhodit","Абиссинская скважина (игла): когда подходит, а когда нет","абиссинская скважина","СЧ",""),
("skvazhina-osnovy","pasport-skvazhiny-chto-v-nem","Паспорт скважины: что в нём и зачем хранить","паспорт скважины на воду","НЧ",""),
("skvazhina-osnovy","skolko-sluzhit-skvazhina","Сколько служит скважина и от чего это зависит","сколько служит скважина","НЧ",""),
("skvazhina-osnovy","debit-skvazhiny-skolko-vody","Дебит скважины: сколько воды хватит для дома","дебит скважины","НЧ",""),
("skvazhina-osnovy","staticheskij-i-dinamicheskij-uroven-vody","Статический и динамический уровень воды простыми словами","динамический уровень воды в скважине","НЧ",""),
("skvazhina-osnovy","nuzhna-li-licenziya-na-skvazhinu","Нужна ли лицензия на скважину для частного дома","нужна ли лицензия на скважину","СЧ",""),
("skvazhina-osnovy","licenziya-na-skvazhinu-v-snt","Лицензия на скважину в СНТ: кто оформляет и что грозит без неё","лицензия на скважину в снт","СЧ",""),
("skvazhina-osnovy","shtraf-za-skvazhinu-bez-licenzii","Штраф за скважину без лицензии: суммы и кому реально грозит","штраф за скважину без лицензии","НЧ",""),
("skvazhina-osnovy","normy-rasstoyaniya-skvazhina-septik-dom-zabor","Нормы: расстояние от скважины до септика, дома и забора","расстояние от скважины до септика","СЧ",""),
("skvazhina-osnovy","mozhno-li-burit-skvazhinu-zimoj","Можно ли бурить скважину зимой","можно ли бурить скважину зимой","НЧ",""),
("skvazhina-osnovy","skvazhina-vnutri-doma-plyusy-minusy","Скважина в подвале дома: плюсы, минусы, ошибки","скважина в подвале дома","НЧ",""),
("skvazhina-osnovy","kak-vybrat-burovuyu-kompaniyu","Как выбрать буровую компанию и не попасть на обман","как выбрать буровую компанию","СЧ",""),
("skvazhina-osnovy","obman-pri-burenii-skvazhin","Схемы обмана при бурении: недобур, пластик без обсадки, «долив воды»","обман при бурении скважин","СЧ",""),
("skvazhina-osnovy","probureli-a-vody-net-nedobur","Пробурили, а воды нет: что такое недобур и как от него защититься","бурение без воды","НЧ",""),
("skvazhina-osnovy","razvedochnoe-burenie-kogda-nuzhno","Разведочное бурение: когда нужно и сколько стоит","разведочное бурение скважины","НЧ",""),
("skvazhina-osnovy","skvazhina-ne-daet-vodu-chto-delat","Скважина перестала давать воду: причины и что делать","скважина не даёт воду","СЧ",""),
("skvazhina-osnovy","upal-napor-vody-iz-skvazhiny","Упал напор воды из скважины: диагностика по шагам","упал напор воды из скважины","НЧ",""),
("skvazhina-osnovy","pesok-v-vode-iz-skvazhiny","Песок в воде из скважины: почему и как убрать","песок в воде из скважины","НЧ",""),
("skvazhina-osnovy","skvazhina-zaililas-vosstanovlenie","Скважина заилилась: признаки и восстановление","скважина заилилась","НЧ",""),

# --- Бурение и обустройство ---
("skvazhina-montazh","obustrojstvo-skvazhiny-adapter-ili-kesson","Обустройство скважины: адаптер или кессон — что выбрать","обустройство скважины адаптер или кессон","СЧ",""),
("skvazhina-montazh","skvazhinnyj-adapter-ustrojstvo-montazh","Скважинный адаптер: устройство, монтаж, срок службы","скважинный адаптер","СЧ",""),
("skvazhina-montazh","kesson-dlya-skvazhiny-plastik-ili-metall","Кессон для скважины: пластиковый или металлический","кессон для скважины пластиковый или металлический","СЧ",""),
("skvazhina-montazh","letnee-obustrojstvo-skvazhiny","Летнее обустройство скважины для дачи на тёплый сезон","летнее обустройство скважины","НЧ",""),
("skvazhina-montazh","vvod-vody-v-dom-ot-skvazhiny","Как завести воду в дом от скважины","завести воду в дом от скважины","СЧ",""),
("skvazhina-montazh","montazh-nasosa-v-skvazhinu","Монтаж скважинного насоса: как подбирают и на какую глубину ставят","установка насоса в скважину","СЧ",""),
("skvazhina-montazh","kak-podobrat-skvazhinnyj-nasos","Как подобрать насос для скважины по глубине и напору","как подобрать насос для скважины","НЧ",""),
("skvazhina-montazh","gidroakkumulyator-i-avtomatika","Гидроаккумулятор и автоматика: зачем нужны и как выбрать объём","установка гидроаккумулятора","НЧ",""),
("skvazhina-montazh","greyushchij-kabel-dlya-vvoda-vody","Греющий кабель для ввода воды: когда он обязателен","греющий кабель для ввода воды","НЧ",""),
("skvazhina-montazh","glubina-promerzaniya-grunta-podmoskovje","Глубина промерзания грунта в Подмосковье и ввод воды в дом","глубина промерзания грунта московская область","НЧ",""),
("skvazhina-montazh","obustrojstvo-skvazhiny-svoimi-rukami","Обустройство скважины своими руками с адаптером: риски и подводные камни","обустройство скважины своими руками","СЧ",""),
("skvazhina-montazh","kesson-pri-vysokom-ugv","Кессон при высоких грунтовых водах: пучение, якорение, обратная засыпка","кессон при высоких грунтовых водах","НЧ",""),

# --- Вода и фильтры (инфо; услуга фильтрации — [решить]) ---
("filtraciya","rzhavaya-voda-iz-skvazhiny-chto-delat","Ржавая вода из скважины: причины и что делать","ржавая вода из скважины","СЧ",""),
("filtraciya","zhelezo-v-vode-iz-skvazhiny","Железо в воде из скважины: чем опасно и как убрать","железо в воде из скважины","СЧ",""),
("filtraciya","zhestkaya-voda-priznaki-posledstviya","Жёсткая вода в доме: признаки и последствия для техники","жёсткая вода признаки","СЧ",""),
("filtraciya","zapah-serovodoroda-v-vode-iz-skvazhiny","Запах сероводорода из скважины: причины и решение","запах сероводорода из скважины","НЧ",""),
("filtraciya","mutnaya-voda-iz-skvazhiny-prichiny","Мутная вода из скважины: разбор причин","мутная вода из скважины","СЧ",""),
("filtraciya","analiz-vody-iz-skvazhiny","Анализ воды из скважины: какие показатели и где сдать","анализ воды из скважины","СЧ",""),
("filtraciya","kak-podobrat-filtr-po-analizu-vody","Как подобрать фильтр для воды по анализу","как подобрать фильтр для воды","НЧ",""),
("filtraciya","obezzhelezivanie-vody-kak-rabotaet","Обезжелезивание воды: как работает система","обезжелезивание воды из скважины","СЧ",""),
("filtraciya","umyagchenie-vody-ot-zhestkosti","Умягчение воды: фильтр против жёсткости","умягчение воды","СЧ",""),
("filtraciya","vodopodgotovka-dlya-zagorodnogo-doma","Водоподготовка для загородного дома: из чего состоит система","водоподготовка для загородного дома","СЧ",""),

# --- Септик: базовое ---
("septik-osnovy","chto-takoe-septik-prostymi-slovami","Что такое септик простыми словами","что такое септик","СЧ",""),
("septik-osnovy","kak-rabotaet-septik-princip-ochistki","Как работает септик: принцип очистки","как работает септик","СЧ",""),
("septik-osnovy","septik-ili-vygrebnaya-yama","Септик или выгребная яма: что выгоднее","септик или выгребная яма","ВЧ",""),
("septik-osnovy","septik-ili-stanciya-bioochistki","Септик или станция биологической очистки: в чём разница","септик или станция биологической очистки","СЧ",""),
("septik-osnovy","septik-ili-betonnye-kolca","Септик или бетонные кольца: честное сравнение","септик или бетонные кольца","СЧ",""),
("septik-osnovy","nakopitelnyj-ili-pererabatyvayushchij-septik","Накопительный или перерабатывающий септик","накопительный или перерабатывающий септик","НЧ",""),
("septik-osnovy","energonezavisimyj-septik","Энергонезависимый септик: где оправдан и как выбрать","энергонезависимый септик","СЧ",""),
("septik-osnovy","stepen-ochistki-septika-kuda-sbrasyvat","Степень очистки септика: куда можно сбрасывать воду","степень очистки септика","НЧ",""),
("septik-osnovy","kuda-slivat-vodu-iz-septika","Куда девать очищенную воду из септика: варианты отвода","куда сливать воду из септика","СЧ",""),
("septik-osnovy","pole-filtracii-i-drenazhnyj-kolodec","Поле фильтрации и дренажный колодец: при глине и высоком УГВ","поле фильтрации для септика","СЧ",""),
("septik-osnovy","normy-ustanovki-septika","Нормы установки септика: расстояния до дома, забора, скважины","нормы установки септика","СЧ",""),
("septik-osnovy","razreshenie-na-septik-i-pravila-snt","Нужно ли разрешение на септик и правила для СНТ","разрешение на септик","СЧ",""),

# --- Выбор и сравнение септиков ---
("septik-vybor","kak-vybrat-septik-dlya-dachi","Как выбрать септик для дачи","как выбрать септик для дачи","ВЧ",""),
("septik-vybor","kak-vybrat-septik-dlya-doma-pmzh","Как выбрать септик для дома с постоянным проживанием","септик для дома постоянного проживания","СЧ",""),
("septik-vybor","kakoj-septik-pri-vysokom-ugv","Какой септик при высоких грунтовых водах","какой септик при высоком уровне грунтовых вод","СЧ",""),
("septik-vybor","kakoj-septik-na-glinistom-grunte","Какой септик на глинистом грунте","септик на глине какой выбрать","НЧ",""),
("septik-vybor","septik-dlya-sezonnoj-dachi","Септик для сезонной дачи: что учесть при простоях","септик для сезонной дачи","НЧ",""),
("septik-vybor","kak-rasschitat-obem-septika","Как рассчитать объём септика по числу людей и залповому сбросу","объём септика как рассчитать","СЧ",""),
("septik-vybor","septik-na-3-4-5-6-chelovek","Септик на 3, 4, 5 и 6 человек: как понять свой размер","септик на 4 человека","СЧ",""),
("septik-vybor","septik-malahit-obzor","Септик «Малахит»: устройство, обслуживание, для каких участков","септик малахит отзывы","СЧ",""),
("septik-vybor","septik-topas-obzor","Септик «Топас»: плюсы, минусы, стоимость обслуживания","септик топас обзор","СЧ",""),
("septik-vybor","septik-astra-yunilos-obzor","Септик «Астра» (Юнилос): обзор","септик астра обзор","СЧ",""),
("septik-vybor","septik-evrolos-obzor","Септик «Евролос»: обзор линейки","септик евролос обзор","СЧ",""),
("septik-vybor","sravnenie-topas-astra-evrolos","Топас, Астра, Евролос: сравнение и что выбрать","сравнение топас астра евролос","СЧ",""),
("septik-vybor","oshibki-pri-vybore-septika","7 ошибок при выборе септика","ошибки при выборе септика","НЧ",""),

# --- Монтаж септика ---
("septik-montazh","montazh-septika-pod-klyuch-etapy","Монтаж септика под ключ: этапы работ","монтаж септика этапы","СЧ",""),
("septik-montazh","ustanovka-septika-zimoj","Установка септика зимой: можно ли и что учесть","установка септика зимой","НЧ",""),
("septik-montazh","kotlovan-pod-septik","Котлован под септик: размеры, копка вручную или экскаватором","котлован для септика","НЧ",""),
("septik-montazh","obratnaya-zasypka-septika","Обратная засыпка септика: почему нельзя обычным грунтом","обратная засыпка септика","НЧ",""),
("septik-montazh","yakorenie-septika","Якорение септика: когда нужно и как делается","якорение септика","НЧ",""),
("septik-montazh","podklyuchenie-septika-k-domu","Подключение септика к дому: трубы, уклон, глубина","подключение септика к дому","СЧ",""),
("septik-montazh","ventilyaciya-septika-i-fanovyj-stoyak","Вентиляция септика и фановый стояк: зачем и как","вентиляция септика","НЧ",""),
("septik-montazh","septik-do-ili-posle-stroitelstva-doma","Ставить септик до или после стройки дома","септик до или после строительства","НЧ",""),
("septik-montazh","glubina-zalozheniya-septika","На какую глубину закапывают септик","глубина заложения септика","НЧ",""),
("septik-montazh","montazh-septika-svoimi-rukami-oshibki","Монтаж септика своими руками: где чаще всего ошибаются","монтаж септика своими руками","СЧ",""),

# --- Эксплуатация септика ---
("septik-ekspluataciya","obsluzhivanie-septika","Обслуживание септика: что и как часто делать","обслуживание септика","СЧ",""),
("septik-ekspluataciya","otkachka-septika-kak-chasto","Как часто откачивать септик","откачка септика как часто","СЧ",""),
("septik-ekspluataciya","bakterii-dlya-septika-nuzhny-li","Бактерии для септика: нужны ли и какие","бактерии для септика","СЧ",""),
("septik-ekspluataciya","chto-nelzya-slivat-v-septik","Что нельзя сливать в септик","что нельзя сливать в септик","СЧ",""),
("septik-ekspluataciya","septik-i-bytovaya-himiya","Септик и бытовая химия: что можно, а что убивает бактерии","септик и бытовая химия","НЧ",""),
("septik-ekspluataciya","konservaciya-septika-na-zimu","Консервация септика на зиму: пошагово","консервация септика на зиму","СЧ",""),
("septik-ekspluataciya","zapah-ot-septika-prichiny","Запах от септика: причины и как убрать","запах от септика","СЧ",""),
("septik-ekspluataciya","iz-septika-ne-uhodit-voda","Из септика не уходит вода: причины и что делать","септик не уходит вода","СЧ",""),
("septik-ekspluataciya","septik-perepolnilsya-chto-delat","Септик переполнился: что делать","септик переполнился","НЧ",""),
("septik-ekspluataciya","septik-vsplyl-iz-zemli","Септик всплыл из земли: почему и как исправить","септик всплыл","НЧ",""),
("septik-ekspluataciya","septik-zamerz-zimoj","Септик замёрз зимой: как разморозить и не допустить","септик замёрз зимой","НЧ",""),
("septik-ekspluataciya","pena-v-septike","Пена в септике: причина и решение","пена в септике","НЧ",""),
("septik-ekspluataciya","moshki-v-septike","Мошки в септике: откуда берутся и как избавиться","мошки в септике","НЧ",""),
("septik-ekspluataciya","septik-shumit-ili-vibriruet","Септик шумит или вибрирует: проверяем компрессор","септик шумит","НЧ",""),
("septik-ekspluataciya","zapusk-septika-posle-prostoya","Как запустить септик после долгого простоя","септик после простоя","НЧ",""),

# --- Опорные (коммерческие, без гео) ---
("skvazhina-osnovy","burenie-skvazhin-na-vodu-v-podmoskovje","Бурение скважин на воду в Подмосковье: как всё устроено","бурение скважин на воду","ВЧ",""),
("skvazhina-montazh","obustrojstvo-skvazhin-pod-klyuch","Обустройство скважин под ключ: составы и варианты","обустройство скважины под ключ","СЧ",""),
("septik-montazh","septik-pod-klyuch-chto-vhodit","Септик под ключ: что входит в работы","септик под ключ","ВЧ",""),
("skvazhina-osnovy","burenie-skvazhin-mgbu","Бурение скважин малогабаритной установкой (МГБУ): когда это единственный вариант","бурение скважины малогабаритной установкой","СЧ",""),
("skvazhina-osnovy","vyezd-inzhenera-na-uchastok","Выезд инженера на участок: что он определяет до бурения","выезд инженера на участок","НЧ",""),

# ================= ФАЗА 2 (после согласования) =================
("skvazhina-cena","skolko-stoit-proburit-skvazhinu","Сколько стоит пробурить скважину в Подмосковье","сколько стоит пробурить скважину","ВЧ","price"),
("skvazhina-cena","skolko-stoit-skvazhina-30-40-50-metrov","Сколько стоит скважина 30, 40, 50 метров под ключ","сколько стоит скважина 50 метров","СЧ","price"),
("skvazhina-cena","cena-obustrojstva-skvazhiny","Сколько стоит обустроить скважину: адаптер, кессон, летний","стоимость обустройства скважины","СЧ","price"),
("septik-cena","skolko-stoit-septik-pod-klyuch","Сколько стоит септик под ключ","сколько стоит септик под ключ","СЧ","price"),
("skvazhina-geo","burenie-skvazhin-GOROD","Бурение скважин в [город] под ключ — шаблон гео-страницы","бурение скважин [город]","СЧ","geo"),
("septik-geo","septik-pod-klyuch-GOROD","Септик под ключ в [город] — шаблон гео-страницы","септик под ключ [город]","СЧ","geo"),
("skvazhina-osnovy","reanimaciya-skvazhiny","Реанимация скважины: методы и когда это оправдано","реанимация скважины","НЧ","decision"),
]


def main():
    rows = []
    for i, (cluster, slug, title, q, tier, gate) in enumerate(PLAN, 1):
        rows.append({
            "id": f"{i:03d}",
            "phase": "2" if gate else "1",
            "cluster": cluster,
            "slug": slug,
            "title": title,
            "target_query": q,
            "tier": tier,
            "gate": gate,
            "status": "план",
        })

    with (ROOT / "content_plan.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    p1 = [r for r in rows if r["phase"] == "1"]
    p2 = [r for r in rows if r["phase"] == "2"]

    lines = ["# Контент-план блога Гидро-С", "",
             f"Всего в плане: **{len(rows)}**. Фаза 1 (пишем сразу): **{len(p1)}**. "
             f"Фаза 2 (после согласований): **{len(p2)}**.", "",
             "Фаза 1 — информационные и опорные статьи: без гео-комбинаторики, без жёстких цен, "
             "не требуют решений владельца. Это стартовый массив под индексацию.", ""]
    by_cluster = {}
    for r in p1:
        by_cluster.setdefault(r["cluster"], []).append(r)
    for cl, items in by_cluster.items():
        lines.append(f"## {cl} ({len(items)})")
        for r in items:
            lines.append(f"- **{r['title']}** — `{r['slug']}` — запрос: _{r['target_query']}_ ({r['tier']})")
        lines.append("")
    lines.append("## Фаза 2 — под согласование")
    for r in p2:
        why = {"price": "нужен утверждённый прайс",
               "geo": "нужен список стоп-локаций + прайс",
               "decision": "решение владельца по услуге"}[r["gate"]]
        lines.append(f"- **{r['title']}** — {why}")
    lines.append("")
    (ROOT / "PLAN.md").write_text("\n".join(lines), encoding="utf-8")

    print(f"content_plan.csv + PLAN.md: {len(rows)} тем (Фаза1={len(p1)}, Фаза2={len(p2)})")


if __name__ == "__main__":
    main()
