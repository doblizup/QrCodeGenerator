import wx
import os
import math
from PIL import Image
from code_generator import QrCodeGenerator
import wx.lib.scrolledpanel as scroller

FRAME_WIDTH = 600
FRAME_HEIGHT = 750

BUTTON_WIDTH = 100
BUTTON_HEIGHT = 30

LIST_BOX_URL_WIDTH = 300
LIST_BOX_URL_HEIGHT = 150

SCROLL_PANEL_WIDTH = 300
SCROLL_PANEL_HEIGHT = 400

TEXT_WIDTH = 300
TEXT_HEIGHT = 30

IMG_WIDTH = 200
IMG_HEIGHT = 200



class QrWindow(wx.Frame):

    def __init__(self):
        super(QrWindow, self).__init__(None, title='QrCodeGenerator',
                                        size=(FRAME_WIDTH, FRAME_HEIGHT))
        
        self.panel = wx.Panel(self)

        self.dirname = ''
        self.url = ''
        self.path = None
        self.qr_code_color = '#000000'
        self.input_array = []
        self.url_index_array = []
        
        self.CreateStatusBar()

        self.__create_menu()
        self.__create_scrollpanels()
        self.__create_buttons()

        
        self.Show(True)
        

    def __create_menu(self):
        # Setting up the menu
        filemenu = wx.Menu()

        menu_about = filemenu.Append(wx.ID_ABOUT, "About")
        menu_about.SetItemLabel("&About")
        filemenu.AppendSeparator()
        menu_exit = filemenu.Append(wx.ID_EXIT, "&Exit", "Exit")

        # Creating Menu Bar
        menu_bar = wx.MenuBar()
        menu_bar.Append(filemenu, "&Menu")
        self.SetMenuBar(menu_bar)

        # Set events
        self.Bind(wx.EVT_MENU, self.on_about, menu_about)
        self.Bind(wx.EVT_MENU, self.on_exit, menu_exit)


    def __create_scrollpanels(self):
        text_pos_x = int(FRAME_WIDTH/2 - TEXT_WIDTH/2)
        button_pos_x = int(FRAME_WIDTH/2 + TEXT_WIDTH/2 + 10)
        list_box_x = int(FRAME_WIDTH/2 - TEXT_WIDTH/2)
        scroll_panel_x = int(FRAME_WIDTH/2 - TEXT_WIDTH/2)

        self.button_add = wx.Button(self.panel, -1, 'Add URL', pos=(button_pos_x, 0), size=(BUTTON_WIDTH, BUTTON_HEIGHT))
        self.button_add.Bind(wx.EVT_BUTTON, self.on_url_input)

        self.url_input = wx.TextCtrl(self.panel, -1, style = wx.TE_PROCESS_ENTER, pos=(text_pos_x, 0), size=(TEXT_WIDTH, TEXT_HEIGHT))
        self.url_input.Bind(wx.EVT_TEXT_ENTER, self.on_url_input)

        self.list_box_url = wx.ListBox(self.panel, -1, pos=(list_box_x, 50), size=(LIST_BOX_URL_WIDTH, LIST_BOX_URL_HEIGHT), style=wx.LB_MULTIPLE)
        self.list_box_url.Bind(wx.EVT_LISTBOX, self.on_url_select)

        self.scroll_panel = scroller.ScrolledPanel(self.panel, -1, pos=(scroll_panel_x, 250), size=(SCROLL_PANEL_WIDTH, SCROLL_PANEL_HEIGHT), style=wx.SIMPLE_BORDER)
        self.scroll_panel.SetupScrolling(scroll_x=False)
        self.scroll_panel.SetBackgroundColour('#FFFFFF')


    def __create_buttons(self):
        button_pos_x = int(FRAME_WIDTH/2 + TEXT_WIDTH/2 + 10)

        self.button_image = wx.Button(self.panel, -1, 'Select image..', pos=(button_pos_x, 50), size=(BUTTON_WIDTH, BUTTON_HEIGHT))
        self.button_image.Bind(wx.EVT_BUTTON, self.on_image)

        self.button_color = wx.Button(self.panel, -1, 'Choose color', pos=(button_pos_x, 100), size=(BUTTON_WIDTH, BUTTON_HEIGHT))
        self.button_color.Bind(wx.EVT_BUTTON, self.on_color)
        
        self.button_qr = wx.Button(self.panel, -1, 'Create QR-Code', pos=(button_pos_x, 150), size=(BUTTON_WIDTH, BUTTON_HEIGHT))
        font = self.button_qr.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)  
        self.button_qr.SetFont(font)
        self.button_qr.SetForegroundColour(wx.Colour(0, 128, 0))
        self.button_qr.Bind(wx.EVT_BUTTON, self.on_qr)


    def on_about(self, e):
        dlg = wx.MessageDialog(self, "A simple QrCodegenerator", "About", wx.OK)
        
        dlg.ShowModal()
        dlg.Destroy()
        

    def on_exit(self, e):
        self.Close(True)
        

    def on_url_input(self, e):
        self.url = self.url_input.GetValue()

        if self.url != '':
            self.list_box_url.Append(self.url)
            self.input_array.append(self.url)
            self.url_input.SetValue('')
            print(self.input_array)
        else:
            self.url_input.SetHint('Please enter an url.')
        


    def on_url_select(self, e):
        self.url_index_array = self.list_box_url.GetSelections()

    def on_image(self, e):
        """
        Open a file
        """
        dlg = wx.FileDialog(self, "Choose an image", self.dirname, "", "*.*", wx.FD_OPEN)
        
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            
            self.path = os.path.join(self.dirname, self.filename)
            print(self.path)
            
        dlg.Destroy()


    def on_color(self, e):
        dlg = wx.ColourDialog(self)

        # SetChooseFull for extended windows visualization
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            self.qr_code_color = dlg.GetColourData().GetColour().GetAsString(wx.C2S_HTML_SYNTAX)

        print(self.qr_code_color)
        print(type(self.qr_code_color))


    def on_qr(self, e):
        qr_width = IMG_WIDTH
        qr_height = IMG_HEIGHT
        panel_width, panel_height = self.scroll_panel.GetSize()
        x_offset = (panel_width - qr_width) // 2  
        y_offset = 0  
        scroll_cnt = 0
        bitmaps = self.scroll_panel.GetChildren()
    
        # deleting old qr on create new
        for bitmap in bitmaps:
            bitmap.Destroy()

        if len(self.url_index_array) != 0:
            for index in self.url_index_array:
                code_generator = QrCodeGenerator(url=self.input_array[index],
                                                image_path=self.path if self.path is not None else None,
                                                qr_color=self.qr_code_color if self.qr_code_color is not None else None)

                qr_code = code_generator.generate_code()
                
                # convert PIL Pic to wx Pic
                qr_image = wx.Image(qr_code.size[0], qr_code.size[1])
                qr_image.SetData(qr_code.convert("RGB").tobytes())

                # scale img
                scaled_image = qr_image.Scale(qr_width, qr_height, wx.IMAGE_QUALITY_HIGH)
                scaled_bitmap = wx.Bitmap(scaled_image)

                # calc pos of qr
                x_pos = x_offset
                y_pos = y_offset + qr_height * scroll_cnt

                # show qr
                wx.StaticBitmap(self.scroll_panel, bitmap=scaled_bitmap, pos=(x_pos, y_pos))

                scroll_cnt += 1

            # calc size of panel scroll
            total_height = qr_height * len(self.url_index_array)
            self.scroll_panel.SetVirtualSize((panel_width, total_height))
        
        else:
            wx.MessageBox('Bitte wählen Sie eine oder mehrere URLs aus.', 'Hinweis', wx.OK|wx.ICON_INFORMATION)


        

if __name__ == '__main__':
    app = wx.App()
    frame = QrWindow()
    app.MainLoop()
