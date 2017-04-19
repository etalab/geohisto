"""Special cases handled manually."""
import inspect

from geohisto import specials
from .constants import DELTA, END_DATETIME
from .utils import compute_id, only_if_depcom


@only_if_depcom('49092')
def _special_case_chemille_en_anjou(towns):
    """Special case: items order where last is not the last in historiq.

    https://www.insee.fr/fr/metadonnees/cog/commune/COM49092-Chemille
    https://www.insee.fr/fr/metadonnees/cog/commune/COM49092-Chemille-Melay
    https://www.insee.fr/fr/metadonnees/cog/commune/COM49092-Chemille-en-Anjou
    """
    chemille, chemille_melay, chemille_en_anjou = towns.filter(depcom='49092')
    chemille_new = chemille.replace_successor(
        chemille_en_anjou.id, chemille_melay.id
    )
    towns.upsert(chemille_new)
    chemille_melay_new = chemille_melay.generate(
        end_datetime=chemille_en_anjou.start_datetime - DELTA,
        successors=chemille_en_anjou.id
    )
    towns.upsert(chemille_melay_new)
    # Then manually update references to successors.
    cosse_anjou = towns.filter(depcom='49111')[0]
    cosse_anjou_new = cosse_anjou.generate(successors=chemille_en_anjou.id)
    towns.upsert(cosse_anjou_new)
    jumeliere = towns.filter(depcom='49169')[0]
    jumeliere_new = jumeliere.generate(successors=chemille_en_anjou.id)
    towns.upsert(jumeliere_new)
    neuvy = towns.filter(depcom='49225')[0]
    neuvy_new = neuvy.generate(successors=chemille_en_anjou.id)
    towns.upsert(neuvy_new)
    christine = towns.filter(depcom='49268')[0]
    christine_new = christine.generate(successors=chemille_en_anjou.id)
    towns.upsert(christine_new)
    georges = towns.filter(depcom='49281')[1]
    georges_new = georges.generate(successors=chemille_en_anjou.id)
    towns.upsert(georges_new)
    lezin = towns.filter(depcom='49300')[0]
    lezin_new = lezin.generate(successors=chemille_en_anjou.id)
    towns.upsert(lezin_new)
    vihiers = towns.filter(depcom='49325')[0]
    vihiers_new = vihiers.generate(successors=chemille_en_anjou.id)
    towns.upsert(vihiers_new)
    tourlandry = towns.filter(depcom='49351')[0]
    tourlandry_new = tourlandry.generate(successors=chemille_en_anjou.id)
    towns.upsert(tourlandry_new)
    valanjou = towns.filter(depcom='49153')[1]
    valanjou_new = valanjou.generate(successors=chemille_en_anjou.id)
    towns.upsert(valanjou_new)


@only_if_depcom('25123')
def _special_case_charbonnieres_sapins(towns):
    """Special case: town changed and successor does not exist yet."""
    charbonnieres_sapins = towns.filter(depcom='25123')[0]
    charbonnieres_sapins_new = charbonnieres_sapins.replace_successor(
        'COM25222@1942-01-01', 'COM25222@2017-01-01')
    towns.upsert(charbonnieres_sapins_new)


@only_if_depcom('28131')
def _special_case_dommerville(towns):
    """Special case: county changed and successor not updated."""
    dommerville_current = towns.filter(depcom='28131')[0]
    dommerville_new = dommerville_current.replace_successor(
        'COM91016@1942-01-01', 'COM91016@1968-01-01')
    towns.upsert(dommerville_new)


@only_if_depcom('69274')
def _special_case_crepieux_pape(towns):
    """Special case: county changed and successor not updated."""
    crepieux_current = towns.filter(depcom='69274')[0]
    crepieux_new = crepieux_current.replace_successor(
        'COM69286@1942-01-01', 'COM69286@1972-12-15')
    towns.upsert(crepieux_new)


@only_if_depcom('91173')
def _special_case_congerville(towns):
    """Special case: county changed and id not updated."""
    congerville_current = towns.filter(depcom='91173')[0]
    congerville_new = congerville_current.replace_successor(
        'COM91613@1942-01-01', 'COM91613@1974-01-01')
    towns.upsert(congerville_new)


@only_if_depcom('95065')
def _special_case_blamecourt(towns):
    """Special case: county changed and successor not updated.

    Giving it a 1ms lifespan given that it does not exist anymore.

    It is a bit ambiguous on INSEE website:
    * https://www.insee.fr/fr/metadonnees/cog/commune/COM95065-Blamecourt
    * https://www.insee.fr/fr/metadonnees/cog/commune/COM78065-Blamecourt
    """
    blamecourt_current = towns.filter(depcom='95065')[0]
    blamecourt_new = blamecourt_current.generate(
        end_datetime=blamecourt_current.start_datetime + DELTA
    )
    blamecourt_new = blamecourt_new.replace_successor(
        'COM95355@1942-01-01', 'COM95355@1968-01-01')
    towns.upsert(blamecourt_new)


@only_if_depcom('95025')
def _special_case_arthieul(towns):
    """Special case: county changed and successor not updated.

    Giving it a 1ms lifespan given that it does not exist anymore.

    It is a bit ambiguous on INSEE website:
    * https://www.insee.fr/fr/metadonnees/cog/commune/COM95025-Arthieul
    * https://www.insee.fr/fr/metadonnees/cog/commune/COM78025-Arthieul
    """
    arthieul_current = towns.filter(depcom='95025')[0]
    arthieul_new = arthieul_current.generate(
        end_datetime=arthieul_current.start_datetime + DELTA
    )
    arthieul_new = arthieul_new.replace_successor(
        'COM95355@1942-01-01', 'COM95355@1968-01-01')
    towns.upsert(arthieul_new)


@only_if_depcom('20366')
def _special_case_chisa(towns):
    """Special case: county changed and id not updated."""
    chisa_wrong, chisa_old = towns.filter(depcom='20366')
    chisa_new = chisa_wrong.generate(id='COM2B366@1976-01-01')
    towns.upsert(chisa_new)
    towns.delete(chisa_wrong)


@only_if_depcom('78692')
def _special_case_butry_oise(towns):
    """Special case: county changed and id not updated."""
    butry_oise_wrong, butry_oise_old = towns.filter(depcom='78692')
    butry_oise_new = butry_oise_wrong.generate(id='COM95120@1968-01-01')
    towns.upsert(butry_oise_new)
    towns.delete(butry_oise_wrong)


@only_if_depcom('2A325')
def _special_case_tivolaggio(towns):
    """Special case: county changed and successor does not exist."""
    tivolaggio = towns.filter(depcom='2A325')[0]
    tivolaggio = tivolaggio.replace_successor(
        'COM2A249@1976-01-01', 'COM20249@1942-01-01')
    towns.upsert(tivolaggio)


@only_if_depcom('25319')
def _special_case_labergement(towns):
    """Special case: successor change on same date."""
    labergement = towns.filter(depcom='25319')[0]
    labergement = labergement.replace_successor(
        'COM25334@1942-01-01', 'COM25334@2017-01-01')
    towns.upsert(labergement)


@only_if_depcom('27688')
def _special_case_villalet(towns):
    """Special case: successor change on same date."""
    villalet = towns.filter(depcom='27688')[0]
    villalet = villalet.replace_successor(
        'COM27693@1972-10-01', 'COM27693@2016-01-01')
    towns.upsert(villalet)


@only_if_depcom('28297')
def _special_case_pezy(towns):
    """Special case: successor change on same date."""
    pezy = towns.filter(depcom='28297')[0]
    pezy = pezy.replace_successor(
        'COM28383@1942-01-01', 'COM28383@2016-01-01')
    towns.upsert(pezy)


@only_if_depcom('88392')
def _special_case_rocourt(towns):
    """Special case: successor change on same date."""
    rocourt = towns.filter(depcom='88392')[0]
    rocourt = rocourt.replace_successor(
        'COM88475@1942-01-01', 'COM88475@2017-01-01')
    towns.upsert(rocourt)


@only_if_depcom('22103')
def _special_case_langrolay(towns):
    """Special case: successor change on same date."""
    langrolay, langrolay_rance, langrolay_rance2 = towns.filter(depcom='22103')
    langrolay_rance = langrolay_rance.replace_successor(
        'COM22213@1942-01-01', 'COM22213@1973-03-15')
    towns.upsert(langrolay_rance)


@only_if_depcom('77316')
def _special_case_orvanne(towns):
    """Special case: too many modifications.

    https://www.insee.fr/fr/metadonnees/cog/commune/COM77316-Orvanne
    https://www.insee.fr/fr/metadonnees/cog/commune/COM77316-Moret-sur-Loing
    https://www.insee.fr/fr/metadonnees/cog/commune/COM77316-Moret-Loing-et-Orvanne
    """
    moret, orvanne, moret_orvanne, with_hyphens = towns.filter(depcom='77316')
    moret_new = moret.replace_successor(
        moret_orvanne.id, orvanne.id
    )
    towns.upsert(moret_new)
    orvanne_new = orvanne.generate(
        end_datetime=moret_orvanne.start_datetime - DELTA,
        successors=moret_orvanne.id
    )
    towns.upsert(orvanne_new)
    moret_orvanne_new = moret_orvanne.generate(
        end_datetime=with_hyphens.start_datetime - DELTA,
        successors=with_hyphens.id
    )
    towns.upsert(moret_orvanne_new)
    # Then manually update references to successors.
    ecuelles = towns.filter(depcom='77166')[0]
    ecuelles_new = ecuelles.generate(successors=orvanne.id)
    towns.upsert(ecuelles_new)
    veneux = towns.filter(depcom='77491')[0]
    veneux_new = veneux.generate(successors=with_hyphens.id)
    towns.upsert(veneux_new)


@only_if_depcom('14475')
def _special_case_noyers(towns):
    """Special case: too many modifications.

    https://www.insee.fr/fr/metadonnees/cog/commune/COM14475-Noyers
    https://www.insee.fr/fr/metadonnees/cog/commune/COM14475-Noyers-Bocage
    https://www.insee.fr/fr/metadonnees/cog/commune/COM14432-Missy
    https://www.insee.fr/fr/metadonnees/cog/commune/COM14475-Noyers-Missy
    https://www.insee.fr/fr/metadonnees/cog/commune/COM14373-Le-Locheur
    https://www.insee.fr/fr/metadonnees/cog/commune/COM14702-Tournay-sur-Odon
    https://www.insee.fr/fr/metadonnees/cog/commune/COM14475-Val-d-Arry
    """
    noyers, bocage, noyers_missy, val_arry = towns.filter(depcom='14475')
    bocage_new = bocage.replace_successor(
        val_arry.id, noyers_missy.id
    )
    towns.upsert(bocage_new)
    noyers_missy_new = noyers_missy.generate(
        end_datetime=val_arry.start_datetime - DELTA,
        successors=val_arry.id
    )
    towns.upsert(noyers_missy_new)
    # Then manually update references to successors.
    missy = towns.filter(depcom='14432')[0]
    missy_new = missy.generate(successors=noyers_missy.id)
    towns.upsert(missy_new)
    tournay_odon = towns.filter(depcom='14702')[1]
    tournay_odon_new = tournay_odon.generate(successors=val_arry.id)
    towns.upsert(tournay_odon_new)


@only_if_depcom('49220')
def _special_case_morannes(towns):
    """Special case: too many modifications.

    https://www.insee.fr/fr/metadonnees/cog/commune/COM49220-Morannes
    https://www.insee.fr/fr/metadonnees/cog/commune/COM49093-Chemire-sur-Sarthe
    https://www.insee.fr/fr/metadonnees/cog/commune/COM49220-Morannes-sur-Sarthe
    https://www.insee.fr/fr/metadonnees/cog/commune/COM49119-Daumeray
    https://www.insee.fr/fr/metadonnees/cog/commune/COM49220-Morannes-sur-Sarthe-Daumeray
    """
    morannes, morannes_daumeray = towns.filter(depcom='49220')
    sur_sarthe = morannes.generate(
        id=compute_id(morannes.depcom, morannes.end_date + DELTA),
        start_datetime=morannes.end_datetime + DELTA,
        end_datetime=morannes_daumeray.start_datetime - DELTA,
        successors=morannes_daumeray.id
    )
    towns.upsert(sur_sarthe)
    morannes_new = morannes.replace_successor(
        morannes_daumeray.id, sur_sarthe.id
    )
    towns.upsert(morannes_new)
    # Then manually update references to successors.
    chemire_sarthe = towns.filter(depcom='49093')[0]
    chemire_sarthe_new = chemire_sarthe.generate(successors=sur_sarthe.id)
    towns.upsert(chemire_sarthe_new)


@only_if_depcom('55245')
def _special_case_madine(towns):
    """Special case: too many modifications.

    https://www.insee.fr/fr/metadonnees/cog/commune/COM55273-Lamarche-en-Woevre
    https://www.insee.fr/fr/metadonnees/cog/commune/COM55386-Nonsard
    https://www.insee.fr/fr/metadonnees/cog/commune/COM55245-Heudicourt-sous-les-Cotes
    https://www.insee.fr/fr/metadonnees/cog/commune/COM55245-Madine
    https://www.insee.fr/fr/metadonnees/cog/commune/COM55386-Nonsard-Lamarche
    """
    heudicourt1, madine, heudicourt2 = towns.filter(depcom='55245')
    lamarche1, lamarche2 = towns.filter(depcom='55273')
    nonsard, nonsard_lamarche = towns.filter(depcom='55386')
    successors = ';'.join([heudicourt2.id, lamarche2.id, nonsard_lamarche.id])
    madine_new = madine.generate(successors=successors)
    towns.upsert(madine_new)
    nonsard_new = nonsard.generate(
        end_datetime=madine.start_datetime - DELTA,
        successors=madine.id
    )
    towns.upsert(nonsard_new)
    lamarche2_new = lamarche2.generate(successors=nonsard_lamarche.id)
    towns.upsert(lamarche2_new)


@only_if_depcom('24362')
def _special_case_saint_alvere(towns):
    """Special case: too many modifications.

    https://www.insee.fr/fr/metadonnees/cog/commune/COM24362-Saint-Alvere
    https://www.insee.fr/fr/metadonnees/cog/commune/COM24362-Sainte-Alvere
    https://www.insee.fr/fr/metadonnees/cog/commune/COM24435-Saint-Laurent-des-Batons
    https://www.insee.fr/fr/metadonnees/cog/commune/COM24362-Sainte-Alvere-Saint-Laurent-Les-Batons
    https://www.insee.fr/fr/metadonnees/cog/commune/COM24092-Cendrieux
    https://www.insee.fr/fr/metadonnees/cog/commune/COM24362-Val-de-Louyre-et-Caudeau
    """
    st, ste_alvere, st_laurent, val_louyre = towns.filter(depcom='24362')
    ste_alvere_new = ste_alvere.generate(successors=st_laurent.id)
    towns.upsert(ste_alvere_new)
    st_laurent_new = st_laurent.generate(
        end_datetime=val_louyre.start_datetime - DELTA,
        successors=val_louyre.id
    )
    towns.upsert(st_laurent_new)


def compute_specials(towns):
    """Apply all special case functions from that file."""
    for name, func in inspect.getmembers(specials, inspect.isfunction):
        if name.startswith('_special_case_'):
            func(towns)
