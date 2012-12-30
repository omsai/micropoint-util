'''
Andor MicroPoint attenuator power conversion utility.

Help support different software applications by converting between:
- 90 divisions of attenuation slider (non-linear).
- % transmission value (linear).
Also displays the power order of magnitude.
'''

__author__ = "Pariksheet Nanda"
__email__ = "p.nanda@andor.com"


from numpy import linspace, log10

from traits.api import HasTraits, Enum, Int, Float, Property
from traitsui.api import View, VGroup, Group, Item, RangeEditor


class MicropointAttenuator(HasTraits):
    type = Enum('Motorized', 'Manual')              
    division = Int(1)
    divisions = Property(Int, depends_on=['type'])
    min_magnitude = Int(0)
    max_magnitude = Property(Int, depends_on=['type'])
    percent_transmission = Property(Float, depends_on=['division', 'type'])
    
    def attenuations(self):
        '''Returns array of transmission values for the mirror
        attenuator specifications.
        '''
        log_attn = linspace(self.min_magnitude,
                            self.max_magnitude,
                            self.divisions)
        linear_attn = 10 ** log_attn
        return linear_attn

    def _get_divisions(self):
        '''Divisions for attenuator type
        '''
        divs = {'Motorized':90, 'Manual':30}
        return divs[self.type]

    def _get_max_magnitude(self):
        '''Orders of magnitude for attenuator type
        '''
        mag = {'Motorized':3, 'Manual':2}
        return mag[self.type]

    def _get_percent_transmission(self):
        '''Read slide rule of laser power transmission
        '''
        attn_array = self.attenuations()
        perc_attn_array = (attn_array / attn_array.max()) * 100
        return perc_attn_array[self.division - 1]

    view = View(
        VGroup(
            Group(
                Item('type', label='Type'),
                Item('divisions', label='Divisions', style='readonly'),
                Item('max_magnitude', label='Orders of Magnitude', style='readonly'),
                label = 'Attenuator Type',
                show_border = True
                ),
            Group(
                Item('division', label='Index',
                     editor=RangeEditor(
                        low=1, high_name='divisions', mode='spinner')),
                Item('percent_transmission',label='Laser Transmission %',
                     style='readonly', format_str = '%.2f'),
                label = 'Attenuator Setting',
                show_border = True
                ),
            ),
        title = 'Micropoint Power',
        )

mp = MicropointAttenuator()
mp.configure_traits()
