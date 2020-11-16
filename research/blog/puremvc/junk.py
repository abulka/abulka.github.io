import wx
import puremvc.interfaces
import puremvc.patterns.facade
import puremvc.patterns.command
import puremvc.patterns.mediator
import puremvc.patterns.proxy


class MyForm(wx.Panel):

    def __init__(self, parent):
    wx.Panel.__init__(self, parent, id=3)
    self.inputFieldTxt = wx.TextCtrl(
        self, -1, size=(170, -1), pos=(5, 10), style=wx.TE_PROCESS_ENTER)


class MyFormMediator(puremvc.patterns.mediator.Mediator, puremvc.interfaces.IMediator):
    NAME = 'MyFormMediator'

    def __init__(self, viewComponent):
    super(MyFormMediator, self).__init__(MyFormMediator.NAME, viewComponent)
    self.viewComponent.Bind(wx.EVT_TEXT_ENTER, self.onSubmit,
                            self.viewComponent.inputFieldTxt)

    def listNotificationInterests(self):
    return [AppFacade.DATA_CHANGED]

    def handleNotification(self, notification):
    if notification.getName() == AppFacade.DATA_CHANGED:
    print "handleNotification (mediator) got", notification.getBody()
    mydata = notification.getBody()
    self.viewComponent.inputFieldTxt.SetValue(mydata)

    def onSubmit(self, evt):
    mydata = self.viewComponent.inputFieldTxt.GetValue()
    self.sendNotification(AppFacade.DATA_SUBMITTED, mydata)


class DataSubmittedCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, notification):
    print "submit execute (command)", notification.getBody()
    mydata = notification.getBody()
    self.datamodelProxy = self.facade.retrieveProxy(DataModelProxy.NAME)
    self.datamodelProxy.setData(mydata.upper())


class DataModelProxy(puremvc.patterns.proxy.Proxy):
    NAME = "DataModelProxy"

    def __init__(self):
    super(DataModelProxy, self).__init__(DataModelProxy.NAME, [])
    self.realdata = Data()
    self.sendNotification(AppFacade.DATA_CHANGED, self.realdata.data)

    def setData(self, data):
    self.realdata.data = data
    print "setData (model) to", data
    self.sendNotification(AppFacade.DATA_CHANGED, self.realdata.data)


class Data:
    def __init__(self):
    self.data = "Hello - hit enter"


class AppFacade(puremvc.patterns.facade.Facade):
    DATA_SUBMITTED = "DATA_SUBMITTED"
    DATA_CHANGED = "DATA_CHANGED"

    @staticmethod
    def getInstance():
    return AppFacade()

    def initializeController(self):
    super(AppFacade, self).initializeController()
    super(AppFacade, self).registerCommand(
        AppFacade.DATA_SUBMITTED, DataSubmittedCommand)


class AppFrame(wx.Frame):
    myForm = None
    mvcfacade = None

    def __init__(self):
    wx.Frame.__init__(self, parent=None, id=-1,
                      title="PureMVC Minimalist Demo", size=(200, 100))
    self.myForm = MyForm(parent=self)
    self.mvcfacade = AppFacade.getInstance()
    self.mvcfacade.registerMediator(MyFormMediator(self.myForm))
    self.mvcfacade.registerProxy(DataModelProxy())


class WxApp(wx.App):
    appFrame = None

    def OnInit(self):
    self.appFrame = AppFrame()
    self.appFrame.Show()
    return True


if __name__ == '__main__':
    wxApp = WxApp(redirect=False)
    wxApp.MainLoop()
