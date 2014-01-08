import passslot

appKey = '<YOUR APP KEY>'
passTemplateId = '<TEMPLATE ID>'

values = {
          'name': 'John',
          'Level': 'Platinum',
          'Balance': 20.50
}

images = {
          'thumbnail': open('thumbnail.png', 'rb')   
}


try:
    engine = passslot.PassSlot.start(appKey)
    pspass = engine.create_pass_from_template(passTemplateId, values, images)
    print(pspass.url)
    
except passslot.PassSlotException as e:
    print('Something went wrong:')
    print(e)