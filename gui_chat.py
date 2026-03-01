import gui_interface, model_interface

if __name__ == '__main__':
    model = model_interface.ModelInterface()
    app = gui_interface.GuiApplication(model=model)
    app.mainloop()
