def scrape():
    # Dependencies
    import pandas as pd
    import requests as req
    from splinter import Browser
    from bs4 import BeautifulSoup as bs
    from webdriver_manager.chrome import ChromeDriverManager

    # Initialize Browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    ## NASA Mars News
    # news_date, news_title, news_body show news information

    url1 = 'https://redplanetscience.com'
    browser.visit(url1)

    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find_all('div',class_="list_text")

    news_date = results[0].find('div',class_='list_date').text
    news_title = results[0].find('div',class_='content_title').text
    news_body = results[0].find('div',class_='article_teaser_body').text


    ## JPL Mars Space Images
    # featured_url is the url showing the featured image

    url2 = 'https://spaceimages-mars.com'
    browser.visit(url2)

    html = browser.html
    soup = bs(html, 'html.parser')

    img_start = 'https://spaceimages-mars.com/'
    img_end = soup.find_all('a',class_='showimg fancybox-thumbs')[0]['href']
    featured_url = img_start+img_end


    ## Mars Facts
    # mars_info is table's html string 

    url3 = 'https://galaxyfacts-mars.com'
    tables = pd.read_html(url3)
    mars_profile = tables[1]
    mars_info = mars_profile.to_html(index=False, header=False, classes='table-striped',table_id='tabtab')


    ## Mars Hemispheres
    # hemi_images is a list of dicts containing full-res photos of Mars Hemispheres

    url4 = 'https://marshemispheres.com/'
    browser.visit(url4)

    hemi_images = []

    html = browser.html
    soup = bs(html, 'html.parser')

    links_found = browser.links.find_by_partial_text('Enhanced')

    for x in range(len(links_found)):
        browser.visit(url4)
        links_found = browser.links.find_by_partial_text('Enhanced')

        links_found[x].click()
        html = browser.html
        soup = bs(html, 'html.parser')

        end_url = soup.find_all('a',target="_blank")[2]['href']
        hemi_url = url4+end_url
        title = soup.find('h2',class_='title').text

        hemi_images.append({'title':title,'hemi_url':hemi_url})

    browser.quit()

    mars_dict = {'news_date':news_date,
                 'news_title':news_title,
                 'news_body':news_body,
                 'featured_url':featured_url,
                 'mars_info':mars_info,
                 'hemi_images':hemi_images
                }

    return mars_dict