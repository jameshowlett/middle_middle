import pandas as pd

from collections import OrderedDict
from math import pi


from bokeh.io import output_notebook, show, vform
from bokeh.charts import Bar, output_file, show
from bokeh.plotting import figure, show, output_file, ColumnDataSource, vplot, hplot
from bokeh.models import (
    CustomJS, ColumnDataSource, SingleIntervalTicker, Slider, HoverTool,
    FactorRange, LinearAxis, CategoricalAxis, BoxAnnotation, GlyphRenderer,
    Legend, Text, Circle, Range1d, Plot, Rect, Square
    )

def make_datasources_for_poverty_comparison(idd_dataframe, years):
    #  stacked bar graph with share of ages PVTAA[2..6]
    poverty_age_codes = ['PVTAA' + str(x+2) for x in xrange(4)]
    
    return make_datasources_for_comparison(idd_dataframe, years, poverty_age_codes)

def make_datasources_for_age_comparison(idd_dataframe, years):
    #  stacked bar graph with share of ages SHA[1..7]
    age_share_codes = ['SHA' + str(x+1) for x in xrange(7)]
    
    return make_datasources_for_comparison(idd_dataframe, years, age_share_codes)

def make_datasources_for_comparison(idd_dataframe, years, measure_codes):
    
    # filter out SHAx measures calculated with METH2012
    row_filter = (idd_dataframe.methodo == '0') & (idd_dataframe.measure_code.isin(measure_codes))                

    bar_charts = []
    countries = set()
    sources = {}
    
    for year in years:
        chart_data = idd_dataframe[row_filter & (idd_dataframe.year == year)]
        
        [countries.add(x) for x in chart_data.location_name.unique()]
        
        bar = Bar(data=chart_data,
                  stack='measure_name',
                  values='observation',
                  label='location_name',
                  legend='top_right',
                  bar_width=1)

        bar_charts.append(bar)
        
        base_source_df = \
            pd.concat([x.to_df() for x in bar.select(dict(type=ColumnDataSource))])
    
        sources['_' + year] = ColumnDataSource(base_source_df)  

    # return the dictionary of ColumnDataSources and 1 bar chart --
    # we want to keep a bar chart so we can reconstruct the legend, later
    return sources, bar_charts[0], countries

def make_interactive_comparison_barchart(sources, bar, countries, years, title,
                                         default_year='2012', show_plot=True,
                                         legend_x=1, legend_x_padding=7.5,
                                         legend_y=[1.12, 1.05], legend_max_x_items=4):

    # define PlotObjects that are common for all years
    xdr = list(countries)
    xdr = FactorRange(factors=sorted(xdr))
    ydr = Range1d(0,1.2) 

    AXIS_FORMATS = dict(
        minor_tick_in=None,
        minor_tick_out=None,
        major_tick_in=None,
        major_label_text_font_size="10pt",
        major_label_text_font_style="normal",
        axis_label_text_font_size="10pt",

        axis_line_color='#AAAAAA',
        major_tick_line_color='#AAAAAA',
        major_label_text_color='#666666',

        major_tick_line_cap="round",
        axis_line_cap="round",
        axis_line_width=1,
        major_tick_line_width=1,
    )

    plot = Plot(plot_width=800,
                plot_height=375,
                x_range = xdr,
                y_range=ydr,
                title = title + default_year,
                outline_line_color=None,
                toolbar_location=None,
                responsive=True)

    xaxis = CategoricalAxis(major_label_orientation = pi/4, axis_label="", **AXIS_FORMATS)
    yaxis = LinearAxis(SingleIntervalTicker(interval=0.2), axis_label="", **AXIS_FORMATS)
    plot.add_layout(xaxis, 'below')
    plot.add_layout(yaxis, 'left')
    
    # create 'reference' source data 
    # 1. this is the ColumnDataSource that has all the glyph info from
    # our previously made BarCharts
    # 2. it should clone a data-source from `sources` otherwise an moving
    # the slider back to '2012' will fail to trigger an update since the
    # new and old `reference_source` ColumnDataSource objects will be the same!
    reference_source = sources['_' + default_year].clone()

    plot.add_glyph(reference_source, \
                   Rect(x='x', y='y', width='width', height='height',\
                        fill_color='color', fill_alpha='fill_alpha'))
    
    # --- add legend --- #
    # This is why we kept one barchart around. It's 'Legend' renderer has all
    # the coloring and text info we want. So we'll have to rip it out
    # and manually make our own legend with glyphs
    
    bar_legend = bar.select(dict(type=Legend))[0].clone()

    tmp_source = []
    for index, legend in enumerate(bar_legend.legends):
        legend_text = legend[0]
        glyph = legend[1][0]
        x = legend_x + legend_x_padding*(index % legend_max_x_items)
        y = legend_y[0] if (index < legend_max_x_items) else legend_y[1]
        tmp_source.append(pd.DataFrame(dict(
                x=x,
                y=y,
                legend_text=legend_text,
                color=glyph.data_source.to_df().color
            )))

    tmp_source = ColumnDataSource(pd.concat(tmp_source))
    plot.add_glyph(tmp_source, Text(x='x', y='y', text='legend_text', text_baseline='bottom', x_offset=10, y_offset=8))
    plot.add_glyph(tmp_source, Square(x='x', y='y', size=10, line_color=None, fill_color='color'))
    
    # --- add HoverTool --- #
    
    hover = HoverTool(point_policy = "snap_to_data") # options "follow_mouse", "snap_to_data")
    hover.tooltips = OrderedDict([
        ("Country", "@x"),
        ("Share", "@height{0.000}")
        ])
    plot.add_tools(hover)
    
    # --- JS callback ---- #

    dictionary_of_sources = dict(zip([x for x in years], ['_%s' % x for x in years]))
    js_source_array = str(dictionary_of_sources).replace("'", "")

    # Add the slider
    code = """
        var year = slider.get('value'),
            sources = %s,
            new_source_data = sources[year].get('data');
        plot.set('title', '%s' + year);
        renderer_source.set('data', new_source_data);
        renderer_source.trigger('change');
    """ % (js_source_array, title)
    
    callback = CustomJS(args=sources, code=code)
    callback.args["plot"] = plot
    callback.args["renderer_source"] = reference_source

    slider = Slider(start=int(years[0]),
                    end=int(years[-1]),
                    value=int(default_year),
                    step=1,
                    orientation='horizontal',
                    title="Year",
                    callback=callback)
    callback.args["slider"] = slider

    # --- put it all together --- #
    layout = vplot(plot, slider)

    if show_plot:
        show(layout)

    return layout