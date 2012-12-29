'''
Andor MicroPoint motorized attenuator power conversion utility.

Help support different software applications by converting between:
- 90 divisions of attenuation slider (non-linear).
- % transmission value (linear).
Also displays the power order of magnitude.
'''

__author__ = "Pariksheet Nanda"
__email__ = "p.nanda@andor.com"


from numpy import linspace, log10

from traits.api import HasTraits, Range, Float, Property
from traitsui.api import View, Group, Item


class MicropointAttenuator(HasTraits):
    def __init__(self, divisions=90, min_magnitude=0,
                 max_magnitude=3, **traits):
        HasTraits.__init__(self, **traits)
        self.add_trait('division',
                       Range(low=1, high=divisions, value=1,
                             mode='spinner'))
        self.divisions = divisions
        self.min_magnitude = min_magnitude
        self.max_magnitude = max_magnitude
    
    percent_transmission = Property(Float, depends_on=['division'])
    
    def attenuations(self):
        '''Returns array of transmission values for the mirror
        attenuator specifications.
        '''
        log_attn = linspace(self.min_magnitude,
                            self.max_magnitude,
                            self.divisions)
        linear_attn = 10 ** log_attn
        return linear_attn

    def _get_percent_transmission(self):
        attn_array = self.attenuations()
        perc_attn_array = (attn_array / attn_array.max()) * 100
        return perc_attn_array[self.division - 1]

    view = View(
        Group(
            Item('division', label='Index'),
            Item('percent_transmission',label='Laser Transmission %',
                 style='readonly', format_str = '%.2f'),
            label = 'Attenuator Setting',
            show_border = True
            ),
        title = 'Micropoint Power',
        )

# If you want to simulate a manual attenuator, you could initialize
# something like:
#
# mp = MicropointAttenuator(divisions=30)
#
# TODO: It would be nice to have a radio button in the UI to toggle
# between manual and motorized presets.
mp = MicropointAttenuator()
mp.configure_traits()
