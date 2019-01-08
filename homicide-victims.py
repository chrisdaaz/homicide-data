

# returns the Victim heading from page
victim = soup.find("h2", string="Victim")

#returns all tds after the Victim heading
victim.find_all_next("td", limit=10)
