import matplotlib.pyplot as plt, numpy as np, os, pandas as pd
from .pathify import *
from .yml import *
import matplotlib

SUBPLOT_ROWS = 'subplot_rows'
SUBPLOT_COLS = 'subplot_cols'
SUPTITLE = 'suptitle'
FIGSIZE = 'figsize'
DPI = 'dpi'
EXTENSIONS = 'extensions'
X = 'x'
Y = 'y'
SHAREX = 'sharex'
SHAREY = 'sharey'
XLABEL = 'xlabel'
YLABEL = 'ylabel'
TITLE = 'title'
XMIN = 'xmin'
XMAX = 'xmax'
YMIN = 'ymin'
YMAX = 'ymax'
GRID = 'grid'
FONT = 'font'
LINEWIDTH = 'linewidth'
SUPTITLE_WEIGHT = 'suptitle-weight'
TITLE_WEIGHT = 'title-weight'

class Plot:
    x = None
    y = None
    should_subplot = False
    should_sharex = False
    should_sharey = False
    linewidth = 1
    suptitle_weight = None
    title_weight = None
    axes = []
    def __init__(self, path_to_config_file):
        self.cwd = path_to_config_file
        self.cfg = yml().load(path_to_config_file/"plot.yml")
        self.run()
    
    def run(self):
        self.set_subplots()
        self.set_suptitle()
        self.set_figsize()
        self.set_dpi()
        self.set_font()
        self.parse_directory()
        plt.tight_layout()
        self.fig.savefig(self.cwd/"plot.png")
        
    def set_subplots(self):
        if SUBPLOT_ROWS in self.cfg and SUBPLOT_COLS in self.cfg:
            self.subplot_rows = self.cfg[SUBPLOT_ROWS]
            self.subplot_cols = self.cfg[SUBPLOT_COLS]
            self.get_sharex()
            self.get_sharey()
            if self.should_sharex:
                if self.should_sharey:
                    self.fig, self.ax = plt.subplots(self.subplot_rows,self.subplot_cols, sharex=True, sharey=True)
                else:
                    self.fig, self.ax = plt.subplots(self.subplot_rows,self.subplot_cols, sharex=True)
            else:
                if self.should_sharey:
                    self.fig, self.ax = plt.subplots(self.subplot_rows,self.subplot_cols, sharey=True)
                else:
                    self.fig, self.ax = plt.subplots(self.subplot_rows,self.subplot_cols)
            self.should_subplot = True
        else:
            self.should_subplot = False

    def get_suptitle_weight(self):
        if SUPTITLE_WEIGHT in self.cfg:
            self.suptitle_weight = self.cfg[SUPTITLE_WEIGHT]

    def set_suptitle(self):
        self.get_suptitle_weight()
        if SUPTITLE in self.cfg:
            if self.suptitle_weight != None:
                plt.suptitle(self.cfg[SUPTITLE], fontweight=self.suptitle_weight)
            else:
                plt.suptitle(self.cfg[SUPTITLE])
    
    def set_figsize(self):
        if FIGSIZE in self.cfg:
            figsize = self.cfg[FIGSIZE]
            if 'ppt' in figsize:
                self.fig.set_figheight(7.5)
                self.fig.set_figwidth(13.333)
    
    def set_dpi(self):
        if DPI in self.cfg:
            self.fig.set_dpi(self.cfg[DPI])

    def get_y(self):
        if Y in self.cfg:
            self.y = self.cfg[Y]
    
    def get_x(self):
        if X in self.cfg:
            self.x = self.cfg[X]

    def parse_directory(self):
        plot_counter = 1
        files = os.listdir(self.cwd)
        files.sort()
        for self.file in files:
            if EXTENSIONS in self.cfg:
                for self.extension in self.cfg[EXTENSIONS]:
                    if self.extension in self.file:
                        if 'csv' in self.extension:
                            df = pd.read_csv(self.cwd/self.file)
                            if self.should_subplot:
                                self.axes.append(plt.subplot(self.subplot_rows, self.subplot_cols, plot_counter))
                            self.get_y()
                            self.get_x()
                            self.set_title()
                            self.set_xlabel()
                            self.set_ylabel()
                            self.y_values = list(df[self.y[0]])
                            if self.x == None:
                                self.x_values = list(np.arange(len(self.y_values)))
                            else:
                                self.x_values = list(df[self.x[0]])
                            self.set_linewidth()
                            plt.plot(self.x_values,self.y_values, linewidth=self.linewidth)
                            self.set_xlim()
                            self.set_ylim()
                            self.set_grid()

                        plot_counter += 1
        if self.should_subplot:
            num_plots = self.subplot_rows * self.subplot_cols
            if plot_counter <= num_plots:
                for i in range(plot_counter,num_plots+1):
                    self.fig.delaxes(self.ax.flatten()[i-1])
    def get_title_weight(self):
        if TITLE_WEIGHT in self.cfg:
            self.title_weight = self.cfg[TITLE_WEIGHT]

    def set_title(self):
        self.get_title_weight()
        if TITLE in self.cfg:
            self.title = self.cfg[TITLE]
            if self.title == 'filename':
                self.title = self.file.replace(self.extension,'')
            if self.title_weight != None:
                plt.title(self.title, fontweight=self.title_weight)
            else:
                plt.title(self.title)

    def get_sharex(self):
        if SHAREX in self.cfg:
            self.should_sharex = self.cfg[SHAREX]

    def get_sharey(self):
        if SHAREY in self.cfg:
            self.should_sharey = self.cfg[SHAREY]

    def set_xlabel(self):
        if XLABEL in self.cfg:
            x_label = self.cfg[XLABEL]
            plt.xlabel(x_label)

    def set_ylabel(self):
        if YLABEL in self.cfg:
            y_label = self.cfg[YLABEL]
            plt.ylabel(y_label)

    def set_xlim(self):
        if XMIN in self.cfg:
            self.xmin = self.cfg[XMIN]
            plt.xlim(left=self.xmin)
        if XMAX in self.cfg:
            self.xmax = self.cfg[XMAX]
            plt.xlim(right=self.xmax)

    def set_ylim(self):
        if YMIN in self.cfg:
            self.ymin = self.cfg[YMIN]
        if YMAX in self.cfg:
            self.ymax = self.cfg[YMAX]
        plt.ylim([self.ymin, self.ymax])

    def set_grid(self):
        if GRID in self.cfg:
            self.axes[-1].grid(True)

    def set_font(self):
        if FONT in self.cfg:
            font = self.cfg[FONT]
            if 'times' in font.lower():
                matplotlib.rcParams['font.sans-serif'] = ['Times New Roman']
                matplotlib.rcParams['axes.unicode_minus'] = False
            
    def set_linewidth(self):
        if LINEWIDTH in self.cfg:
            self.linewidth = self.cfg[LINEWIDTH]