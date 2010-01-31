import wx
max = 80
dlg = wx.ProgressDialog("Progress dialog example",
                       "An informative message",
                       maximum = max,
                       style = wx.PD_CAN_ABORT
                        | wx.PD_APP_MODAL
                        | wx.PD_ELAPSED_TIME
                        #| wx.PD_ESTIMATED_TIME
                        | wx.PD_REMAINING_TIME
                        )

keepGoing = True
count = 0

while keepGoing and count < max:
    count += 1
    wx.MilliSleep(250)

    if count >= max / 2:
        (keepGoing, skip) = dlg.Update(count, "Half-time!")
    else:
        (keepGoing, skip) = dlg.Update(count)

        
dlg.Destroy()
