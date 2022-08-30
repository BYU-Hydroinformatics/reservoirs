from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import CustomSetting

class Reservoirs_ecuador(TethysAppBase):
    """
    Tethys app class for Reservoirs_ecuador."
    """

    name = 'Reservoirs'
    index = 'reservoirs_ecuador:home'
    icon = 'reservoirs_ecuador/images/logo.jpg'
    package = 'reservoirs_ecuador'
    root_url = 'reservoirs_ecuador'
    color = '#008080'
    description = ''
    tags = ''
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='reservoirs_ecuador',
                controller='reservoirs_ecuador.controllers.home'
            ),
            UrlMap(
                name='getMySites',
                url='getMySites/',
                controller='reservoirs_ecuador.controllers.GetSites'
            ),
            UrlMap(
                name='GetSiteInfo',
                url='GetSiteInfo/',
                controller='reservoirs_ecuador.controllers.GetInfo'
            ),
            UrlMap(
                name='GetSiteInfo2',
                url='GetSiteInfo2/',
                controller='reservoirs_ecuador.controllers.GetInfoReal'
            ),
            UrlMap(
                name='GetValues',
                url='GetValues/',
                controller='reservoirs_ecuador.controllers.GetValues'
            ),
            UrlMap(
                name='GetForecast',
                url='GetForecast/',
                controller='reservoirs_ecuador.controllers.GetForecast'
            ),
            # UrlMap(
            #     name='getTimeSeries',
            #     url='getTimeSeries/',
            #     controller='reservoirs_ecuador.controllers.getTimeSeries'
            # ),
            # UrlMap(
            #     name='getMonthlyAverage',
            #     url='getMonthlyAverage/',
            #     controller='reservoirs_ecuador.controllers.getMonthlyAverage'
            # )
        )

        return url_maps
    def custom_settings(self):
        """
        Example custom_settings method.
        """
        custom_settings = (
            CustomSetting(
                name ='Hydroser_Endpoint',
                type = CustomSetting.TYPE_STRING,
                description = 'Endpoint for the WaterOneFlow web service',
                required = False
            ),
        )

        return custom_settings
