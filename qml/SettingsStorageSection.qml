import QtQuick
import QtQuick.Layouts
import "Components"
import Qt.labs.platform
import io.mrarm.mcpelauncher 1.0

ColumnLayout {
    id: columnlayout
    width: parent.width
    spacing: 10

    MButton {
        text: gameLauncher.running ? qsTr("Import World or Pack") : qsTr("Import World or Pack (pending until launch)")
        Layout.fillWidth: true
        onClicked: filePicker.open()
    }

    FileDialog {
        id: filePicker
        title: qsTr("Please pick the Minecraft file")
        nameFilters: ["Minecraft (*.mcaddon *.mcpack *.mcstructure *.mctemplate *.mcworld)", qsTr("All files (*)")]
        fileMode: FileDialog.OpenFiles

        onAccepted: {
            for (var i = 0; i < filePicker.currentFiles.length; i++) {
                gameLauncher.pendingFiles.push(filePicker.currentFiles[i])
            }
            gameLauncher.importFiles()
        }
    }

    RowLayout {
        Layout.fillWidth: true
        MTextField {
            id: uri
            Layout.fillWidth: true
            text: "minecraft://"
        }
        MButton {
            Layout.maximumHeight: uri.height
            text: gameLauncher.running ? qsTr("Open Uri") : qsTr("Open Uri (pending until launch)")
            onClicked: {
                gameLauncher.pendingFiles.push(uri.text)
                gameLauncher.importFiles()
            }
        }
    }

    HorizontalDivider {}

    MText {
        text: qsTr("Game Directories")
        font.bold: true
        font.pointSize: 11
        Layout.topMargin: 10
    }

    MText {
        text: qsTr("Game directories for current selected profile: ") + (profileManagerInstance.activeProfile.nameLocked && profileManagerInstance.activeProfile.name === "Default" ? qsTr("Default") : profileManagerInstance.activeProfile.name)
        Layout.bottomMargin: 5
    }

    Repeater {
        property string gameDataDir: window.getCurrentGameDataDir()
        model: [{
                "label": qsTr("Data Root"),
                "path": gameDataDir
            }, {
                "label": qsTr("Worlds"),
                "path": gameDataDir + "/games/com.mojang/minecraftWorlds"
            }, {
                "label": qsTr("Resource Packs"),
                "path": gameDataDir + "/games/com.mojang/resource_packs"
            }, {
                "label": qsTr("Behaviour Packs"),
                "path": gameDataDir + "/games/com.mojang/behavior_packs"
            }]
        delegate: pathField
    }

    HorizontalDivider {}

    MText {
        text: qsTr("Default Game Directories")
        font.bold: true
        font.pointSize: 11
        Layout.topMargin: 10
        Layout.bottomMargin: 10
    }

    Repeater {
        property string gameDataDir: window.getCurrentGameDataDir()
        model: [{
                "label": qsTr("Game Data"),
                "path": gameDataDir
            }, {
                "label": qsTr("Versions"),
                "path": gameDataDir + "/versions"
            }]
        delegate: pathField
    }

    Component {
        id: pathField
        Column {
            Layout.fillWidth: true
            Layout.bottomMargin: 5
            spacing: 4
            MText {
                text: qsTr(modelData.label)
                font.bold: true
            }
            RowLayout {
                width: parent.width
                height: 35
                MTextField {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    text: QmlUrlUtils.urlToLocalFile(modelData.path)
                    readOnly: true
                    color: "#aaa"
                    hoverEnabled: false
                }
                MButton {
                    Layout.minimumWidth: 40
                    Layout.fillHeight: true
                    onClicked: Qt.openUrlExternally(modelData.path)
                    Image {
                        anchors.centerIn: parent
                        width: 20
                        height: 20
                        source: "qrc:/Resources/icon-folder.png"
                        smooth: false
                    }
                }
            }
        }
    }
}
