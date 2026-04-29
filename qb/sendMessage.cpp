// g++ sendMessage.cpp -o sendMessage -lshell32

#include <windows.h>
#include <shellapi.h>
#include <stdio.h>

void ShowToast(PCWSTR title, PCWSTR message, int type) {
    NOTIFYICONDATAW nid = {0};
    nid.cbSize = sizeof(NOTIFYICONDATAW);
    nid.hWnd = GetDesktopWindow(); 
    nid.uFlags = NIF_INFO | NIF_ICON;
    
    switch(type) {
        case 1:
            nid.hIcon = LoadIcon(NULL, IDI_WARNING);
            nid.dwInfoFlags = NIIF_WARNING;
            break;
        case 2:
            nid.hIcon = LoadIcon(NULL, IDI_ERROR);
            nid.dwInfoFlags = NIIF_ERROR;
            break;
        default:
            nid.hIcon = LoadIcon(NULL, IDI_INFORMATION);
            nid.dwInfoFlags = NIIF_INFO;
            break;
    }

    wcsncpy(nid.szInfoTitle, title, ARRAYSIZE(nid.szInfoTitle) - 1);
    wcsncpy(nid.szInfo, message, ARRAYSIZE(nid.szInfo) - 1);

    Shell_NotifyIconW(NIM_ADD, &nid);
    Sleep(3000);
    Shell_NotifyIconW(NIM_DELETE, &nid);
}

int main() {
    int argc;
    LPWSTR* argv = CommandLineToArgvW(GetCommandLineW(), &argc);

    if (argv == NULL || argc < 4) {
        wprintf(L"sendMessage.exe \"Title\" \"Text\" Type (0-2)\n");
        wprintf(L"0 - Info, 1 - Warning, 2 - Error\n");
        return 1;
    }

    // argv[0] - name
    // argv[1] - title
    // argv[2] - text
    // argv[3] - type
    PCWSTR title = argv[1];
    PCWSTR message = argv[2];
    int type = _wtoi(argv[3]);

    ShowToast(title, message, type);

    LocalFree(argv);

    return 0;
}