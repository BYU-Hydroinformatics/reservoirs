from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import CustomSetting
from tethys_sdk.workspaces import app_workspace

class Reservoirs(TethysAppBase):
    """
    Tethys app class for Reservoirs."
    """

    name = 'Reservoirs'
    index = 'home'
    icon = 'reservoirs/images/logo.jpg'
    package = 'reservoirs'
    root_url = 'reservoirs'
    color = '#008080'
    description = ''
    tags = ''
    enable_feedback = False
    feedback_emails = []
    controllers_modules = ['controllers']

    # def url_maps(self):
    #     """
    #     Add controllers
    #     """
    #     UrlMap = url_map_maker(self.root_url)
    #
    #     url_maps = (
    #         UrlMap(
    #             name='home',
    #             url='reservoirs',
    #             controller='reservoirs.controllers.home'
    #         ),
    #         UrlMap(
    #             name='getMySites',
    #             url='getMySites/',
    #             controller='reservoirs.controllers.GetSites'
    #         ),
    #         UrlMap(
    #             name='GetInfo',
    #             url='GetInfo/',
    #             controller='reservoirs.controllers.GetInfo'
    #         ),
    #         UrlMap(
    #             name='GetInfo2',
    #             url='GetInfo2/',
    #             controller='reservoirs.controllers.GetInfoReal'
    #         ),
    #         UrlMap(
    #             name='GetValues',
    #             url='GetValues/',
    #             controller='reservoirs.controllers.GetValues'
    #         ),
    #         UrlMap(
    #             name='GetForecast',
    #             url='GetForecast/',
    #             controller='reservoirs.controllers.GetForecast'
    #         ),
    #         # UrlMap(
    #         #     name='getTimeSeries',
    #         #     url='getTimeSeries/',
    #         #     controller='reservoirs.controllers.getTimeSeries'
    #         # ),
    #         # UrlMap(
    #         #     name='getMonthlyAverage',
    #         #     url='getMonthlyAverage/',
    #         #     controller='reservoirs.controllers.getMonthlyAverage'
    #         # )
    #     )
    #
    #     return url_maps
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
