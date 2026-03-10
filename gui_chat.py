import fileio
import gui_interface, model_interface

if __name__ == '__main__':
    #model = model_interface.ModelInterface()
    #app = gui_interface.GuiApplication(model=model)
    #app.mainloop()

    print(fileio.read_conversation_file('conversations/2026-03-05--14-17-21'))
