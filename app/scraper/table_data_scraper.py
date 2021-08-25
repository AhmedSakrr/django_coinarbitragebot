

def scrape_table(
        table,
        model
):
    coins = []
    row_index = 0
    for item in table.find_all('tr'):
        if row_index <= 1:
            row_index += 1
            continue

        tds = item.find_all('td')
        code = tds[0].text.strip()
        name = tds[1].find_all('a')[0].text
        url = 'https://coinarbitragebot.com' + tds[10].find_all('a')[0]['href']
        coin = model.objects.create(
            code=code,
            name=name,
            url=url
        )
        coins.append(coin)

    print(f'{len(coins)} items scrapped')
    return coins
