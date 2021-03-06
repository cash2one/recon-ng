import module

class Module(module.Module):

    def __init__(self, params):
        module.Module.__init__(self, params, query='SELECT DISTINCT street_address FROM locations WHERE street_address IS NOT NULL')
        self.info = {
            'Name': 'Address Geocoder',
            'Author': 'Quentin Kaiser (contact@quentinkaiser.be)',
            'Description': 'Queries the Google Maps API to obtain coordinates for an address. Updates the \'locations\' table with the results.'
        }

    def module_run(self, addresses):
        for address in addresses:
            self.verbose("Geocoding '%s'..." % (address))
            payload = {'address' : address, 'sensor' : 'false'}
            url = 'https://maps.googleapis.com/maps/api/geocode/json'
            resp = self.request(url, payload=payload)
            # kill the module if nothing is returned
            if len(resp.json['results']) == 0:
                self.output('Unable to geocode \'%s\'.' % (address))
                return
            # loop through the results
            for result in resp.json['results']:
                lat = result['geometry']['location']['lat']
                lon = result['geometry']['location']['lng']
                # store the result
                self.add_locations(lat, lon, address)
                # output the result
                self.alert("Latitude: %s, Longitude: %s" % (lat, lon))
            self.query('DELETE FROM locations WHERE street_address=? AND latitude IS NULL AND longitude IS NULL', (address,))
