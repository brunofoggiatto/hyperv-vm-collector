#!/usr/bin/env python3
import winrm
import getpass
import json
import os


def listar_vms(session):
    """Após a conexão com o servidor windows server, onde está virtualizado as vms, faz coleta de métricas."""
    ps_script = """
    Get-VM | ForEach-Object {
        $vm = $_
        $ips = (Get-VMNetworkAdapter -VMName $vm.Name).IPAddresses -join ", "
        [PSCustomObject]@{
            Name = $vm.Name
            State = $vm.State
            RAM_MB = [math]::Round($vm.MemoryAssigned / 1MB)
            CPUCount = $vm.ProcessorCount
            IPAddresses = $ips
        }
    } | ConvertTo-Json
    """

    result = session.run_ps(ps_script)
    return result.std_out.decode().strip()


def main():
    print(" Coletando informações de VMs dos servidores Hyper-V \n")

    # Credenciais
    username = input("Usuário: ").strip()
    password = getpass.getpass("Senha: ")

    # Lê lista de servidores de um arquivo de configuração
    config_path = "config.json"
    if not os.path.exists(config_path):
        print(f"Arquivo '{config_path}' não encontrado. Crie a partir de 'config_example.json'.")
        return

    with open(config_path) as f:
        servidores = json.load(f).get("servers", [])

    todas_vms = []

    for host_ip in servidores:
        print(f"\nConectando a {host_ip} ")
        try:
            session = winrm.Session(host_ip, auth=(username, password), transport='ntlm')
            output_json = listar_vms(session)
            vms = json.loads(output_json)
            for vm in vms:
                vm["Host"] = host_ip
                todas_vms.append(vm)
        except Exception as e:
            print(f"Erro ao coletar dados do servidor {host_ip}: {e}")

    print("\nTodas as VMs (Cluster Unificado) ")
    for vm in todas_vms:
        print(f"{vm['Name']} ({vm['State']}) - RAM: {vm['RAM_MB']}MB, CPUs: {vm['CPUCount']}, "
              f"IPs: {vm['IPAddresses']}, Host: {vm['Host']}")

    print(f"\nTotal de VMs no cluster: {len(todas_vms)}")


if __name__ == "__main__":
    main()
